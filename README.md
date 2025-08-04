# 👤 Enhanced User Account Creation Script

A Python-based utility that reads user account data from a CSV file, validates it, and sends HTTP requests to an API endpoint to create user accounts.

Designed for **data validation**, **error handling**, and **detailed logging**, this script ensures smooth user creation processes for batch inputs.

---

## 🚀 Features

- ✅ **Validation of required fields** (name, email, role)
- 📧 **Email format checking**
- 🛡️ **Role verification** (`admin`, `user`, `moderator`)
- 📊 **Summary report** of created, skipped, and failed entries
- 🪵 **Detailed logging** to `error_log.txt`
- 🔄 **Graceful handling** of API/network errors

---

## 🛠️ How It Works

This script reads a CSV file (`users.csv`), validates each row, and sends a `POST` request to an API to create user accounts. Any invalid rows are skipped with logged warnings.

---

## 📄 CSV Format

Ensure your `users.csv` includes the following headers:

```csv
name,email,role
James Brown,james.brown@example.com,admin
Harsha Wijeratne,harsha.wijeratne@example.com,moderator
Lucía Torres,lucia.torres@example,moderator
````

* **name**: User's full name *(required)*
* **email**: Must be a valid email format *(required)*
* **role**: Must be one of `admin`, `user`, or `moderator` *(required)*

---

## 💻 Setup & Usage

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Place Your CSV File

Place your `users.csv` in the same directory as the script.

### 3. Run the Script

```bash
python user_creator.py
```

---

## 📈 Example Output

Console output:

```
2025-08-03 10:30:15 - INFO - Starting to process file: users.csv
2025-08-03 10:30:15 - WARNING - Row 3 skipped: Missing email - Data: {'name': 'Bob', 'email': '', 'role': 'user'}
2025-08-03 10:30:16 - INFO - User created successfully: alice@example.com
2025-08-03 10:30:16 - ERROR - Row 5 failed: Invalid email format: not-an-email - User: not-an-email
```

Summary:

```
==================================================
PROCESSING COMPLETE
Total rows: 4
Successfully created: 2
Skipped (validation failed): 1
Failed (API errors): 1
```

---

## 📁 Files Created

| File              | Description                         |
| ----------------- | ----------------------------------- |
| `users.csv`       | Input CSV containing user data      |
| `user_creator.py` | The main Python script              |
| `error_log.txt`   | Error + warning log with timestamps |

---

## ⚙️ Configuration

Change these at the bottom of the script:

```python
CSV_FILE = "users.csv"
API_ENDPOINT = "https://example.com/api/create_user"
```

---

## 🧪 Test Data Suggestions

Try users with:

* ✅ Valid email/role
* ❌ Invalid email formats
* ❌ Invalid roles (e.g., `manager`)
* ❌ Missing fields (name/email/role)

---

## ⚠️ Limitations & Improvements

### Current Limitations

* Only basic email validation (`@`, `.` check)
* No retry logic for failed requests
* One-by-one user processing (not optimized for speed)

### Suggestions for improving the script

*  Regex-based email validation
*  Retry API calls on failure
*  Multi-threading or batching
*  Progress bar for large CSV files
*  Config via `.env` or YAML

---

## 🧩 Code Overview

| Function               | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| `setup_logging()`      | Sets up console + file logging                   |
| `validate_user_data()` | Validates CSV row for required fields and format |
| `create_single_user()` | Sends API request to create a user               |
| `create_users()`       | Reads file, processes each user, logs summary    |

---

## 🛠️ Troubleshooting

| Problem                  | Solution                                               |
| ------------------------ | ------------------------------------------------------ |
| **File not found**       | Ensure `users.csv` exists and is correctly named       |
| **Missing CSV columns**  | File must have: `name,email,role` as headers           |
| **Invalid email / role** | Fix CSV values or validate with stricter rules         |
| **API/network failure**  | Verify endpoint, check network, or log for error codes |

---

##Final Summary Results:

Error Logs ← error_log.txt
```
Total rows: 10
Successfully created: 0          ← Expected (test API)
Skipped (validation failed): 4   ← Perfect! Caught all bad data
Failed (API errors): 6           ← Expected (fake API rejecting)
```

