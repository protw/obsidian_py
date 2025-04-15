## How to activate Google Sheets API and Google Drive API in a project

To enable **the Google Sheets API** and **Google Drive API** in your Google Cloud project, follow these steps:

### 1. Open the Google Cloud Console

Go to [the Google Cloud Console](https://console.cloud.google.com/) .

### 2. Choose your project

If you don't have a project yet:

- Click `Choose project`(at the top of the page).
- Press `Create project`, enter a name, and press `Create`.

If the project already exists:

- Click on `Choose project`and select the desired project.

### 3. Activate the Google Sheets API

1. Go to the [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) page .
2. Click `Enable`.

### 4. Activate the Google Drive API

1. Go to the [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) page .
2. Click `Enable`.

### 5. Create Credentials

If you need to access the API through Python or other code:

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials) .
2. Click `Create account data`→ `Create service account`.
3. Fill in the name, click `Create and continue`.
4. Assign the role **Editor** or **Owner** (for full access).
5. Click `Done`.
6. In the list of accounts, find the created account → tap `Edit`→ `Keys`→ `Append key`→ `JSON`.
7. Download the file `credentials.json`you will need to work with the API.

### 6. Add a service account to Google Sheets (if necessary)

If you plan to work with the Google Sheets API:

- Open the desired Google Sheet.
- Share it ( `Grant access`) with **the service account email** (which is listed in `credentials.json`).
- Assign **editing rights** if you need to modify the table.

### 7. Check access

Use Python to check if everything works:

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "credentials.json"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)
print("Google Sheets API activated!")
```

If you see the message `Google Sheets API activated!`, then everything is configured correctly.