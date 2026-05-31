# 🧠 Psychiatric Disorders SRA Dashboard

An interactive, web-based metadata exploration dashboard designed for managing and visualizing Short Read Archive (SRA) and GEO sequencing studies related to Psychiatric Disorders (Schizophrenia, Bipolar Disorder, MDD, Depression).

Built specifically for the AbbVie team to easily track summary statistics, sample demographics, fastq file locations, and pipeline progress.

## ✨ Key Features

- **🔐 Secure Authentication:** Integrated `streamlit-authenticator` to restrict access to authorized team members. Users and hashed passwords are managed locally via `users.yaml`.
- **🔍 Advanced Study Explorer:** Filter through dozens of RNA-seq/genomic studies by disease flag, sample size, or custom search keywords.
- **👥 Sample Demographics:** Dynamically aggregates metadata across 79+ studies into a SQLite database. Automatically generates rich Pie Charts showcasing disease status (Control vs. Schizophrenia) and Gender distributions.
- **📊 Interactive Visualizations:** Utilizes Plotly Express for highly responsive, modern data visualizations with dark-mode aesthetic styling.
- **📥 One-Click Downloads:** Download cleanly formatted sample sheets, metadata trackers, and pipeline info as CSV files directly from the UI.
- **⚙️ Cloud-Ready:** Optimized and configured to deploy seamlessly on Streamlit Community Cloud (with pinned `requirements.txt` and Python `runtime.txt`).

## 🛠️ Technology Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/) (Python)
- **Visualizations:** [Plotly Express](https://plotly.com/python/plotly-express/)
- **Data Processing:** Pandas, NumPy
- **Database:** SQLite3 (`sra_metadata.db`)
- **Environment Management:** [Pixi](https://prefix.dev/) & `pip`
- **Security:** `bcrypt`, `streamlit-authenticator`

## 🚀 Setup & Installation

### Option 1: Using Pixi (Recommended)
This project uses Pixi for fast and deterministic environment management.
```bash
# Clone the repository
git clone https://github.com/Surajsharma95/Psychiatric-Disorders-SRA-Dashboard.git
cd Psychiatric-Disorders-SRA-Dashboard

# Run the app directly (Pixi will handle dependencies automatically)
pixi run streamlit run app.py
```

### Option 2: Using pip (Standard Python)
Ensure you have Python 3.11+ installed.
```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## 📂 Project Structure

```text
├── app.py                         # Main Streamlit application
├── sra_metadata.db                # SQLite DB storing core studies and samples
├── users.yaml                     # Authentication credentials (hashed)
├── requirements.txt               # App dependencies for deployment
├── runtime.txt                    # Specifies Python version for cloud deployment
├── master_sample_metadata.csv     # Aggregated metadata for all samples
├── Summary-tracker - *.csv        # Static CSVs tracking pipeline progress
├── local_scripts/
│   ├── build_master_metadata.py   # Aggregates 79+ local TSVs into SQLite & CSV
│   ├── parse_local_metadata.py    # Utility to parse single local TSV files
│   └── fetch_srp_metadata.py      # Utility to fetch fresh NCBI E-Utils XML data
└── README.md                      # This file
```

## 🧑‍💻 Data Management Workflows

### Updating Sample Metadata
If you download new `*_metadata.tsv` files to your AbbVie metadata folder, you can regenerate the entire dashboard database by running:
```bash
pixi run python local_scripts/build_master_metadata.py
```
This script will parse all local TSVs, extract harmonized disease states and biological attributes, rebuild `master_sample_metadata.csv`, and update the `sample_metadata` table in `sra_metadata.db`.

## ☁️ Deployment

This app is configured for continuous deployment on **Streamlit Community Cloud**. 
Any push to the `main` branch of this repository will automatically trigger a rebuild and redeployment of the live application.
