## Зміст файлу `credentials.json`

Варіант із сервісним акаунтом — це класичний, автоматизований спосіб, який працює без взаємодії користувача.

### 🔑 Приклад `credentials.json`

Файл має ось таку структуру:

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

### Як отримати цей файл?

1. Перейдіть у [Google Cloud Console](https://console.cloud.google.com/).
2. Виберіть ваш проєкт.
3. Перейдіть у **API & Services → Credentials**.
4. Натисніть **Create Credentials → Service Account**.
5. У полі **Role** виберіть:
    - Google Sheets API → **Editor** (або Viewer, якщо тільки читати)
    - Google Drive API → **Reader**
6. Після створення сервісного акаунту:
    - Перейдіть у нього.
    - Вкладка **Keys → Add Key → JSON**.
    - Завантажте файл.

### Важливий момент ⚠️

У таблиці Google Sheets:

1. Відкрий таблицю.
2. Поділися нею через:
    ```
    your-service-account@your-project-id.iam.gserviceaccount.com
    ```
3. Дай права **Редагування** або **Перегляд**.

## Значення полів файлу `credentials.json`

Тут пояснимо докладніше, які поля у файлі **`credentials.json`** визначаються автоматично, а які потрібно заповнювати вручну. 

### Приклад файлу `credentials.json`

Файл **генерується автоматично** під час створення сервісного акаунту, але важливо розуміти, що означає кожне поле.

#### Ось стандартний вигляд:

```json
{
  "type": "service_account",                           ✅ (жорстко визначено)
  "project_id": "your-project-id",                    🔑 (вказує Google Cloud під час створення проєкту)
  "private_key_id": "your-private-key-id",            🔑 (генерується автоматично)
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQ...long_key...\n-----END PRIVATE KEY-----\n",  🔑 (автоматично, закритий ключ RSA)
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",  🔑 (автоматично)
  "client_id": "your-client-id",                      🔑 (автоматично)
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  ✅ (жорстко визначено)
  "token_uri": "https://oauth2.googleapis.com/token", ✅ (жорстко визначено)
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", ✅ (жорстко визначено)
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account@your-project-id.iam.gserviceaccount.com"  🔑 (автоматично)
}
```

### Поля, які генеруються автоматично (нічого не треба чіпати):

| Поле                            | Опис                     | Примітка                   |
| ------------------------------- | ------------------------ | -------------------------- |
| `"type"`                        | Тип ключа                | Завжди `"service_account"` |
| `"auth_uri"`                    | URL для авторизації      | Однаковий для всіх         |
| `"token_uri"`                   | URL для отримання токену | Однаковий для всіх         |
| `"auth_provider_x509_cert_url"` | URL для сертифікатів     | Однаковий для всіх         |

### Поля, які Google генерує автоматично (вам не треба нічого заповнювати):

| Поле               | Опис                              |
| ------------------ | --------------------------------- |
| `"private_key"`    | Закритий ключ для підпису запитів |
| `"private_key_id"` | Ідентифікатор ключа               |
| `"client_email"`   | Email сервісного акаунту          |
| `"client_id"`      | Унікальний ідентифікатор клієнта  |

### Поля, які вам потрібно контролювати:

| Поле                     | Що це?                             | Як заповнити?                                                |
| ------------------------ | ---------------------------------- | ------------------------------------------------------------ |
| `"project_id"`           | Ідентифікатор проєкту              | Google задає сам, але можна побачити у Google Cloud Console (типово: **назва-проєкту-123456**) |
| `"client_email"`         | Email сервісного акаунта           | Додається у таблицю Google Sheets як **співавтор**           |
| `"client_x509_cert_url"` | URL сертифіката сервісного акаунта | Використовується API                                         |

### Найважливіше!

Вам потрібно **вручну лише додати цей email у таблицю Google Sheets**:

```
your-service-account@your-project-id.iam.gserviceaccount.com
```

✅ Доступ: **Editor** або **Viewer**

### Як перевірити email?

1. Відкрий файл `credentials.json`.
2. Скопіюйте значення з:
    ```json
    "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com"
    ```
3. Перейдіть у таблицю.
4. Поділіться доступом:
    - **Налаштування доступу → Запросити доступ → Вставити email**
    - Додайте як **Редактор** або **Переглядач**

