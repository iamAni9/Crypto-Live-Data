# Cryptocurrency Live Data Updater

This project fetches live data for the top 50 cryptocurrencies by market capitalization and updates a Google Sheet every 5 minutes. The data includes:

- **Cryptocurrency Name**
- **Symbol**
- **Current Price (USD)**
- **Market Capitalization**
- **24-hour Trading Volume**
- **24-hour Price Change (percentage)**

Additionally, the sheet includes:

- Top 5 cryptocurrencies by market cap.
- Average price of the top 50 cryptocurrencies.
- Highest and lowest 24-hour percentage price changes.

## Live Google Sheet

You can view the live-updating Google Sheet here: [Live Cryptocurrency Data Sheet](https://docs.google.com/spreadsheets/d/1H7NCkIgLQuQ-N4-B-iLuRYZUzmgEL8rUH9isSVBOKNc/edit?usp=sharing)

## How It Works

The program is running on a free instance, which comes with some limitations. It may stop after a period of inactivity. If the sheet stops updating, you can run the program locally by following the steps below.

## Running the Program Locally

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Set Up a Virtual Environment (Optional)

It’s recommended to use a virtual environment to manage dependencies. Run the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **Google Sheets API** and **Google Drive API** for your project:
   - Navigate to **APIs & Services > Library**.
   - Search for "Google Sheets API" and "Google Drive API" and enable them.
4. Create a service account:
   - Go to **IAM & Admin > Service Accounts**.
   - Click **Create Service Account**.
   - Assign the **Editor** role.
   - Click **Done**.
5. Create and download credentials:
   - In the **Service Accounts** section, click on the newly created account.
   - Go to the **Keys** tab and click **Add Key > Create New Key**.
   - Choose **JSON** and download the key file. Save it as `credentials.json`.

### Step 5: Create a `.env` File

Create a `.env` file in the project root directory and add the following:

```env
GOOGLE_CREDENTIALS='{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account-email@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project.iam.gserviceaccount.com"
}'
```

Replace the values with the ones from your `credentials.json` file.

### Step 6: Share the Google Sheet with the Service Account

1. Open the Google Sheet you want to update.
2. Click the **Share** button.
3. Add the **service account email** (found in your `credentials.json` file) as an **Editor**.

### Step 7: Run the Program

Run the script to start updating the Google Sheet:

```bash
python script.py
```

The program will fetch data every 5 minutes and update the Google Sheet.

## Requirements

The following Python packages are required:

- `gspread`
- `oauth2client`
- `requests`
- `schedule`
- `python-dotenv`

Install them using:

```bash
pip install -r requirements.txt
```

## Notes

- The program is designed to run continuously. If you stop it, the Google Sheet will no longer update.
- The free instance may stop after a period of inactivity. To keep it running, consider upgrading to a paid instance or running the program locally.

## Contributing

If you'd like to contribute to this project, feel free to **open a pull request** or **submit an issue**.

---

**Happy Coding! 🚀**

