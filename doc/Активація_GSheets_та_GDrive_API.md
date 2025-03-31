## Як активувати Google Sheets API та Google Drive API у проєкті

Щоб активувати **Google Sheets API** та **Google Drive API** у своєму проєкті в Google Cloud, виконайте наступні кроки:

### 1. Відкрийте Google Cloud Console

Перейдіть до [Google Cloud Console](https://console.cloud.google.com/).

### 2. Виберіть свій проєкт

Якщо у вас ще немає проєкту:

- Натисніть `Вибір проєкту` (вгорі сторінки).
- Натисніть `Створити проєкт`, задайте назву та натисніть `Створити`.

Якщо проєкт уже є:

- Натисніть на `Вибір проєкту` і оберіть потрібний проєкт.

### 3. Активуйте Google Sheets API

1. Перейдіть на сторінку [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com).
2. Натисніть **"Увімкнути"** (`Enable`).

### 4. Активуйте Google Drive API

1. Перейдіть на сторінку [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com).
2. Натисніть **"Увімкнути"** (`Enable`).

### 5. Створіть облікові дані (Credentials)

Якщо вам потрібно отримати доступ до API через Python або інший код:

1. Перейдіть до [Credentials](https://console.cloud.google.com/apis/credentials).
2. Натисніть `Створити облікові дані` → `Обліковий запис сервісу` (Service Account).
3. Заповніть назву, натисніть `Створити та продовжити`.
4. Призначте роль **Editor** або **Owner** (для повного доступу).
5. Натисніть `Готово`.
6. У списку облікових записів знайдіть створений аккаунт → натисніть `Редагувати` → `Ключі` → `Додати ключ` → `JSON`.
7. Завантажте файл `credentials.json`, який вам знадобиться для роботи з API.

### 6. Додайте сервісний аккаунт до Google Sheets (якщо потрібно)

Якщо ви плануєте працювати з Google Sheets API:

- Відкрийте потрібний Google Sheet.
- Поділіться ним (`Надати доступ`) з **email сервісного аккаунту** (який вказаний у `credentials.json`).
- Призначте **редакторські права**, якщо потрібно змінювати таблицю.

### 7. Перевірте доступ

Використовуйте Python, щоб перевірити, чи все працює:

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "credentials.json"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("sheets", "v4", credentials=creds)
print("Google Sheets API активовано!")
```

Якщо бачите повідомлення `Google Sheets API активовано!`, значить усе налаштовано правильно.