# 🔒 Securely Connecting Streamlit to Private Google Sheets

Since this is AbbVie company data, you **must not** use the "Publish to Web" feature. Instead, we will use a **Google Cloud Service Account**. This acts as a virtual robot user that you can securely share your private Google Sheets with.

## Step 1: Create a Google Cloud Service Account
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Search for **"Google Drive API"** and **"Google Sheets API"** in the top search bar and click **Enable** for both.
4. Navigate to **IAM & Admin > Service Accounts**.
5. Click **Create Service Account**, name it (e.g., `sra-dashboard-bot`), and click Done.
6. Click on the newly created Service Account, go to the **Keys** tab, click **Add Key > Create New Key**, and select **JSON**.
7. The JSON file will download to your computer.

## Step 2: Share your Google Sheet
1. Open the downloaded JSON file and look for the `client_email` field. It will look something like this: `sra-dashboard-bot@your-project-id.iam.gserviceaccount.com`.
2. Go to your private Google Sheet.
3. Click the **Share** button in the top right.
4. Paste the `client_email` and share the sheet as a **Viewer**.

## Step 3: Configure Streamlit Secrets
1. Inside your `Psychiatric-Disorders-SRA-Dashboard` folder, create a `.streamlit` folder and a `secrets.toml` file.
2. Format the `secrets.toml` file EXACTLY like this, pasting the contents of your downloaded JSON file into the `connections.gsheets` section:

```toml
[sheets]
summary_url = "https://docs.google.com/spreadsheets/d/your_summary_sheet_id_here/edit"
pipeline_url = "https://docs.google.com/spreadsheets/d/your_pipeline_sheet_id_here/edit"

[connections.gsheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_LONG_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "sra-dashboard-bot@your-project-id.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-url"
```
*(Make sure the `private_key` includes the `\n` characters instead of actual newlines!)*

Once this is set up, the dashboard will securely and privately fetch the data in the background.
