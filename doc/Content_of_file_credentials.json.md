## File contents `credentials.json`

The service account option is a classic, automated method that works without user interaction.

### 🔑 Example `credentials.json`

The file has the following structure:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBA...long_key...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
}
```

### How do I get this file?

1. Go to [the Google Cloud Console](https://console.cloud.google.com/) .
2. Choose your project.
3. Go to **API & Services → Credentials** .
4. Click **Create Credentials → Service Account** .
5. In the **Role** field, select:
   - Google Sheets API → **Editor** (or Viewer, if read only)
   - Google Drive API → **Reader**
6. After creating a service account:
   - Go to it.
   - Keys tab **→ Add Key → JSON** .
   - Download the file.

### Important point ⚠️

In a Google Sheets table:

1. Open the table.

2. Share it via:

   ```
   your-service-account@your-project-id.iam.gserviceaccount.com
   ```

3. Give **Edit** or **View** permissions .

## File field values`credentials.json`

Here we will explain in more detail which fields in the file **`credentials.json`**are automatically determined and which need to be filled in manually.

### Example file `credentials.json`

The file **is generated automatically** when you create a service account, but it is important to understand what each field means.

#### Here is the standard view:

```json
{
  "type": "service_account",                           ✅ (rigidly defined)
  "project_id": "your-project-id",                    🔑 (specifies Google Cloud when creating a project)
  "private_key_id": "your-private-key-id",            🔑 (generated automatically)
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQ...long_key...\n-----END PRIVATE KEY-----\n",  🔑 (automatic, RSA private key)
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",  🔑 (automatic)
  "client_id": "your-client-id",                      🔑 (automatic)
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  ✅ (rigidly defined)
  "token_uri": "https://oauth2.googleapis.com/token", ✅ (rigidly defined)
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", ✅ (rigidly defined)
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account@your-project-id.iam.gserviceaccount.com"  🔑 (automatic)
}
```

### Fields that are automatically generated (no need to touch anything):

| Field                           | Description           | Note                      |
| ------------------------------- | --------------------- | ------------------------- |
| `"type"`                        | Key type              | Always`"service_account"` |
| `"auth_uri"`                    | URL for authorization | Same for everyone         |
| `"token_uri"`                   | URL to get the token  | Same for everyone         |
| `"auth_provider_x509_cert_url"` | URL for certificates  | Same for everyone         |

### Fields that Google automatically generates (you don't need to fill anything in):

| Field              | Description                      |
| ------------------ | -------------------------------- |
| `"private_key"`    | Private key for signing requests |
| `"private_key_id"` | Key ID                           |
| `"client_email"`   | Service account email            |
| `"client_id"`      | Unique customer identifier       |

### Fields you need to control:

| Field                    | What is it?                     | How to fill it out?                                          |
| ------------------------ | ------------------------------- | ------------------------------------------------------------ |
| `"project_id"`           | Project ID                      | Google sets it itself, but you can see it in the Google Cloud Console (typically: **project-name-123456** ) |
| `"client_email"`         | Service account email           | Added to Google Sheets as **a co-author**                    |
| `"client_x509_cert_url"` | Service account certificate URL | API used                                                     |

### Most importantly!

You **just need to manually add this email to the Google Sheets table**:

```
your-service-account@your-project-id.iam.gserviceaccount.com
```

✅ Access: **Editor** or **Viewer**

### How to check email?

1. Open the file `credentials.json`.

2. Copy the values from:

   ```json
   "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com"
   ```

3. Go to the table.

4. Share access:

   - **Access Settings → Request Access → Insert Email**
   - Add as **Editor** or **Viewer**

 
