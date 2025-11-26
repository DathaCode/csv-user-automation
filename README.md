# 🐳 User Creation Script — Batch User Import via CSV (Docker + Python)

A production-ready, containerized Python tool to **batch-create user accounts** from CSV files via API.

Built for **automation**, **stability**, **logging**, **validation**, and **multi-platform deployment**.

---

## 🚀 Features

- 🐳 **Docker containerized** for consistent deployments  
- 📂 **Batch user creation** from CSV  
- 🔍 **Data validation**  
  - Required fields  
  - Email format  
  - Role validation  
- 📝 **Detailed error + activity logging**  
- ⏱️ **Timeout, retry, and API error handling**  
- 📊 **Processing summary & statistics**  
- 🔒 **Security scanning** with Trivy  
- 🌍 **Multi-platform builds** (amd64, arm64)  

---

## ⚡ Quick Start with Docker

### 1️⃣ Pull the image
```bash
docker pull yourusername/user-creation-script:latest
```

### 2️⃣ Run the container
```bash
docker run --rm \
  -v $(pwd)/users.csv:/app/data/users.csv:ro \
  -v $(pwd)/logs:/app/logs \
  -e API_ENDPOINT=https://your-api.com/create_user \
  yourusername/user-creation-script:latest
```

### 3️⃣ Using Docker Compose

Create `.env`:
```bash
cp .env.example .env
```

Run:
```bash
docker-compose up
```

---

## 🛠️ Makefile Commands (Recommended)

```bash
make help       # Show all commands
make build      # Build Docker image
make run        # Run container
make logs       # View logs
make pull       # Pull Docker Hub image
make push       # Push to Docker Hub
make stop       # Stop running containers
make clean      # Cleanup containers/images
```

---

## 📄 CSV Format

Your CSV **must** contain the following:

| Column | Type   | Required | Valid Values |
|--------|---------|-----------|--------------|
| name   | string | Yes       | Non-empty string |
| email  | string | Yes       | Valid email |
| role   | string | Yes       | admin, user, moderator |

### Example `users.csv`
```csv
name,email,role
John Doe,john@example.com,admin
Jane Smith,jane@example.com,user
Bob Wilson,bob@example.com,moderator
```

---

## 🧑‍💻 Local Development Setup

Clone + install dependencies:
```bash
git clone https://github.com/yourusername/user-creation-script.git
cd user-creation-script

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run locally:
```bash
python user_creation_script.py
```

---

## 🧪 Running Tests

```bash
pytest                       # Run all tests
pytest --cov=. --cov-report=html   # Coverage report
pytest tests/test_user_creation.py -v
```

---

## 🔧 Code Quality & Security

```bash
make format         # Auto-format with Black
make lint           # Lint with Flake8
make security-scan  # Bandit + Safety
```

---

## 🌱 Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `CSV_FILE` | Path to CSV file | `/app/data/users.csv` |
| `API_ENDPOINT` | User creation API endpoint | `https://example.com/api/create_user` |

---

## 🐍 Docker Image Details

- **Base Image:** python:3.11-slim  
- **Optimized multi-stage build**  
- **Size:** ~150MB  
- **Platforms:** linux/amd64, linux/arm64  
- **Runs as:** non-root `appuser`  
- **Healthcheck:** Enabled  

---

## 🤖 CI/CD Pipeline (GitHub Actions)

Includes automated:

### ✔ Lint & Test  
- Black  
- Flake8  
- Pytest (+ coverage)  
- Builds on Python 3.9, 3.10, 3.11  

### ✔ Security  
- Bandit  
- Safety  

### ✔ Docker Build  
- Multi-platform build  
- Trivy vulnerability scanning  
- Tags: `latest`, semantic versions, commit SHA  
- Push to Docker Hub  

### ✔ Docker Verification  
- Pull & run test image  
- Validate health  
- Check image size  

---

## 🔐 Setup GitHub Secrets

Add to Repo → Settings → Secrets:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

Push to start CI/CD deployments:
```bash
git add .
git commit -m "Setup CI/CD"
git push origin main
```

---

## 🐋 Docker Hub Repository

Your images will appear at:

```
https://hub.docker.com/r/yourusername/user-creation-script
```

---

## ❗ Troubleshooting

### ❌ Container exits immediately
```bash
docker-compose logs
```

### ❌ CSV file not found
```bash
ls -la users.csv
```

### ❌ Permission denied
```bash
chmod 644 users.csv
```

### ❌ API errors  
Check connectivity:
```bash
curl -X POST https://your-api.com/create_user
```

---

## 📁 Project Structure

```
.
├── .github/workflows/ci-cd.yml
├── tests/
│   └── test_user_creation.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .dockerignore
├── user_creation_script.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .flake8
├── setup.py
├── .env.example
└── README.md
```

---

## 🤝 Contributing

1. Fork the repo  
2. Create a branch: `git checkout -b feature/my-feature`  
3. Commit changes  
4. Push: `git push origin feature/my-feature`  
5. Open a Pull Request  

---

## 📜 License
MIT License

---

## 💬 Support

- GitHub Issues: https://github.com/yourusername/user-creation-script/issues  
- Docker Hub: https://hub.docker.com/r/yourusername/user-creation-script  

