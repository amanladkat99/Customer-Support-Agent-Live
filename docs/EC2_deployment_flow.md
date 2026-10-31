# EC2 Deployment Flow & GitHub Secrets Setup

This project uses GitHub Actions (`.github/workflows/deploy-ec2.yml`) to automatically test and deploy the Customer Support Agent to an AWS EC2 instance on every push to the `main` branch (or via manual workflow dispatch).

---

## 1. Required GitHub Secrets

In your GitHub repository, navigate to **Settings** → **Secrets and variables** → **Actions** and add the following repository secrets:

| Secret Name | Description | Example Value |
|---|---|---|
| `EC2_HOST` | **Public IP** or **Public DNS** of your EC2 instance (do not include `ssh` or `user@`) | `3.85.123.45` or `ec2-3-85-123-45.compute-1.amazonaws.com` |
| `EC2_USER` | SSH user for your AMI | `ubuntu` (for Ubuntu) or `ec2-user` (for Amazon Linux) |
| `EC2_SSH_KEY` | Private SSH key (`.pem`) used to launch the instance | `-----BEGIN RSA PRIVATE KEY----- ... -----END RSA PRIVATE KEY-----` |
| `EC2_PORT` | *(Optional, default: 22)* SSH Port | `22` |
| `EC2_APP_DIR` | *(Optional, default: `/opt/customer_support_agent`)* Target directory on EC2 | `/opt/customer_support_agent` or `/home/ubuntu/customer_support_agent` |
| `EC2_ENV_FILE` | Full contents of your production `.env` file | *(See Section 3 below)* |

> [!IMPORTANT]
> To automatically create the `.env` file on EC2 during deployment, navigate to **Settings** → **Secrets and variables** → **Actions** → **Variables** tab and add a repository variable:
> - **Name**: `INJECT_ENV_FILE`
> - **Value**: `true`

---

## 2. EC2 Security Group Configuration

Ensure your EC2 instance's **Inbound rules** allow traffic on the following ports:

| Type | Protocol | Port Range | Source | Purpose |
|---|---|---|---|---|
| **SSH** | TCP | `22` | `0.0.0.0/0` | Enables GitHub Actions runner and you to connect via SSH |
| **Custom TCP** | TCP | `8000` | `0.0.0.0/0` | FastAPI backend API |
| **Custom TCP** | TCP | `8501` | `0.0.0.0/0` | Streamlit Dashboard UI |

---

## 3. Required Environment Variables for EC2_ENV_FILE

The `.env` file on the EC2 instance must contain your API keys and configuration:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
OPENAI_API_KEY=your_openai_api_key_here
# Or GOOGLE_API_KEY if using Google embeddings
# GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 4. Deployment Pipeline Workflow

```mermaid
flowchart TD
    A["Push to main / Workflow Dispatch"] --> B["Test Job (Ubuntu Runner)"]
    B --> C["Install Python 3.12 & uv"]
    C --> D["uv sync --dev & run pytest"]
    D --> E["Deploy Job"]
    E --> F["Inject .env (if INJECT_ENV_FILE=true)"]
    F --> G["Package release.tar.gz"]
    G --> H["SCP archive to EC2"]
    H --> I["SSH into EC2: Unpack & run docker compose"]
    I --> J["Verify http://127.0.0.1:8000/health"]
```

