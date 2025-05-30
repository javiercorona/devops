
DevOps Automation Assistant
A FastAPI-based service to generate DevOps artifacts (Terraform, CI/CD, Dockerfiles, Kubernetes YAML, Ansible, CloudFormation, Monitoring configs) via REST API endpoints, with API key protection, persistence, and a static UI.

🚀 Features
Generate Terraform infrastructure code

Generate CI/CD pipeline YAMLs

Generate Dockerfiles & Kubernetes manifests

Generate Ansible playbooks

Generate AWS CloudFormation templates

Generate monitoring configs (e.g., Prometheus)

Save & retrieve generated artifacts

Simple web UI (served from /static)

API key security

📁 Project Structure
arduino
Copy
Edit
devops_assistant/
├── main.py
├── config.ini
├── requirements.txt
├── sources/
│   ├── agents/
│   │   ├── terraform_agent.py
│   │   ├── cicd_agent.py
│   │   └── devops_agent.py
│   ├── database/
│   │   └── db_handler.py
│   └── models/
│       ├── infrastructure.py
│       └── deployment.py
├── static/
│   └── index.html
⚙️ Setup Instructions
Clone the repo

bash
Copy
Edit
git clone <your_repo_url>
cd devops_assistant
Install dependencies
Make sure you have Python 3.8+.

bash
Copy
Edit
pip install -r requirements.txt
Configure API Key
Edit config.ini:

ini
Copy
Edit
[AUTH]
api_key = your-strong-api-key
Run the app

bash
Copy
Edit
uvicorn main:app --reload
By default, the static UI will be available at http://localhost:8000/static/

🔐 Authentication
All API endpoints require an API key header:

vbnet
Copy
Edit
X-API-Key: your-strong-api-key
Set this in your HTTP client (curl/Postman/etc).

🛠️ API Usage
1. Generate Terraform
http
Copy
Edit
POST /generate/terraform
Content-Type: application/json
X-API-Key: your-strong-api-key

{
  // See sources/models/infrastructure.py for the schema
}
2. Generate CI/CD Pipeline
http
Copy
Edit
POST /generate/cicd
Content-Type: application/json
X-API-Key: your-strong-api-key

{
  // See sources/models/deployment.py for the schema
}
3. Generate Dockerfile
http
Copy
Edit
POST /generate/dockerfile
Content-Type: application/json
X-API-Key: your-strong-api-key

{
  "base_image": "python:3.9-slim",
  "port": 8000
}
4. Generate Kubernetes Deployment
http
Copy
Edit
POST /generate/k8s
Content-Type: application/json
X-API-Key: your-strong-api-key

{
  "name": "my-app",
  "image": "my-app:latest",
  "port": 8000
}
5. Generate Ansible Playbook
http
Copy
Edit
POST /generate/ansible
Content-Type: application/json
X-API-Key: your-strong-api-key
6. Generate CloudFormation Template
http
Copy
Edit
POST /generate/cloudformation
Content-Type: application/json
X-API-Key: your-strong-api-key

{
  "stack_name": "my-stack",
  "resources": [ ... ]
}
7. Generate Monitoring Config
http
Copy
Edit
POST /generate/monitoring
Content-Type: application/json
X-API-Key: your-strong-api-key

{
  "system": "prometheus",
  "metrics": [
    {"job_name": "api", "targets": ["localhost:9090"]}
  ]
}
💾 Artifacts API
Save artifact:
POST /artifacts
JSON: { "key": "unique-id", "code": "<artifact code>" }

Retrieve artifact:
GET /artifacts/{key}

List artifact keys:
GET /artifacts

🖥️ Static Web UI
The static UI is served from the static/ folder at http://localhost:8000/static/.

You can add your own HTML/CSS/JS for a custom dashboard.

📝 Example Usage (with curl)
bash
Copy
Edit
curl -X POST http://localhost:8000/generate/dockerfile \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-strong-api-key" \
  -d '{"base_image": "python:3.9-slim", "port": 8000}'
🧩 Extending
Add new artifact generators in sources/agents/.

Update request/response models in sources/models/.

Extend the UI in the static/ folder.

🛡️ Security
Change your API key from the default.

Consider deploying behind HTTPS/reverse proxy in production.

📣 Support
For issues, suggestions, or contributions:
Open a GitHub Issue or Pull Request.

