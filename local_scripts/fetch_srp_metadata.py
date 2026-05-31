import sys
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import pandas as pd
import argparse

def fetch_srp_metadata(srp_id):
    print(f"🔍 Searching NCBI for {srp_id}...")
    
    # 1. Search for the internal SRA ID for the given SRP
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term={srp_id}[Accession]"
    try:
        search_response = urllib.request.urlopen(search_url)
        search_xml = ET.parse(search_response)
        id_node = search_xml.find(".//IdList/Id")
        if id_node is None:
            print(f"❌ Could not find {srp_id} in NCBI SRA database.")
            return None
        internal_id = id_node.text
    except Exception as e:
        print(f"❌ Error searching NCBI: {e}")
        return None
        
    print(f"📥 Fetching metadata for internal ID {internal_id}...")
    # 2. Fetch the full XML for that study
    fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id={internal_id}"
    try:
        fetch_response = urllib.request.urlopen(fetch_url)
        tree = ET.parse(fetch_response)
    except Exception as e:
        print(f"❌ Error fetching XML from NCBI: {e}")
        return None

    records = []
    
    # 3. Parse each Experiment Package
    for exp_pkg in tree.findall('.//EXPERIMENT_PACKAGE'):
        # Get Study
        study = exp_pkg.find('.//STUDY')
        study_acc = study.attrib.get('accession', srp_id) if study is not None else srp_id
        
        # Get Sample
        sample = exp_pkg.find('.//SAMPLE')
        sample_acc = sample.attrib.get('accession', '') if sample is not None else ''
        sample_title = sample.find('TITLE').text if sample is not None and sample.find('TITLE') is not None else ''
        
        organism = ''
        if sample is not None:
            org_node = sample.find('.//SCIENTIFIC_NAME')
            if org_node is not None:
                organism = org_node.text
                
        # Parse all sample attributes (tissue, disease, healthy/control, etc.)
        attributes = {}
        if sample is not None:
            for attr in sample.findall('.//SAMPLE_ATTRIBUTE'):
                tag = attr.find('TAG').text.lower() if attr.find('TAG') is not None else ''
                val = attr.find('VALUE').text if attr.find('VALUE') is not None else ''
                if tag:
                    attributes[tag] = val

        # Get Runs (SRR)
        run_set = exp_pkg.find('.//RUN_SET')
        if run_set is not None:
            for run in run_set.findall('RUN'):
                run_acc = run.attrib.get('accession', '')
                
                # Combine base info with dynamic attributes
                record = {
                    'Study_ID': study_acc,
                    'Run_ID': run_acc,
                    'Sample_ID': sample_acc,
                    'Organism': organism,
                    'Sample_Title': sample_title
                }
                
                # Add all biological attributes dynamically
                for k, v in attributes.items():
                    record[f"attr_{k}"] = v
                    
                records.append(record)

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch SRA metadata for an SRP ID including sample attributes.")
    parser.add_argument("srp_id", help="The SRP accession to fetch (e.g. SRP063852)")
    parser.add_argument("--out", "-o", help="Output CSV filename", default="")
    args = parser.parse_args()
    
    df = fetch_srp_metadata(args.srp_id)
    
    if df is not None and not df.empty:
        out_file = args.out if args.out else f"{args.srp_id}_metadata.csv"
        df.to_csv(out_file, index=False)
        print(f"✅ Successfully fetched {len(df)} SRR runs.")
        print(f"💾 Saved to {out_file}")
        
        # Display a preview of important columns
        print("\n📊 Preview:")
        preview_cols = ['Run_ID', 'Organism', 'Sample_Title']
        # Try to find disease/tissue columns to preview
        attr_cols = [c for c in df.columns if 'disease' in c.lower() or 'health' in c.lower() or 'tissue' in c.lower() or 'diagnosis' in c.lower() or 'source_name' in c.lower()]
        preview_cols.extend(attr_cols[:3]) # show up to 3 relevant attribute columns
        
        print(df[preview_cols].head())
    else:
        print("⚠️ No data found.")
