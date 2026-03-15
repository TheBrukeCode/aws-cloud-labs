# ✅ Serverless Task Manager API

A production-ready serverless REST API built on AWS, demonstrating core cloud architecture patterns including Lambda, API Gateway, and DynamoDB. Built as part of an AWS Solutions Architect portfolio.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                               │
│                                                                 │
│   Client (curl / Postman / Frontend)                            │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────┐                                       │
│   │    API Gateway      │  ◄── API Key Auth + Throttling        │
│   │  (REST API / prod)  │      (100 req/s rate limit)           │
│   └──────────┬──────────┘                                       │
│              │                                                  │
│    ┌─────────┼──────────────────────────────┐                  │
│    │         │   Lambda Functions            │                  │
│    │  POST   ├──► create_task.py            │                  │
│    │  GET    ├──► get_task.py               │                  │
│    │  GET    ├──► list_tasks.py             │                  │
│    │  PUT    ├──► update_task.py            │                  │
│    │  DELETE └──► delete_task.py            │                  │
│    └─────────────────────┬─────────────────┘                  │
│                          │                                      │
│                          ▼                                      │
│              ┌───────────────────────┐                          │
│              │  DynamoDB             │                          │
│              │  Table: tasks         │                          │
│              │  PK: userId (HASH)    │                          │
│              │  SK: taskId (RANGE)   │                          │
│              │  Billing: On-demand   │                          │
│              └───────────────────────┘                          │
│                                                                 │
│   ┌──────────────────────────────────────────┐                 │
│   │ IAM  │ Each Lambda has a least-privilege  │                 │
│   │      │ role — read-only or CRUD per func  │                 │
│   └──────────────────────────────────────────┘                 │
│                                                                 │
│   ┌──────────────────────────────────────────┐                 │
│   │ CloudWatch │ Automatic logs for every     │                 │
│   │            │ Lambda invocation            │                 │
│   └──────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why this architecture?

| Decision | Reason |
|---|---|
| **Lambda over EC2** | No servers to manage; pay only per invocation; scales to zero |
| **DynamoDB over RDS** | Serverless, no connection pooling issues, single-digit ms latency |
| **One Lambda per route** | Least-privilege IAM (read-only Lambdas can't write), independent scaling |
| **SAM for IaC** | Repeatable, version-controlled infrastructure; avoids manual console drift |
| **API Key auth** | Simple auth layer for portfolio; production would use Cognito JWT |

---

## 📁 Project Structure

```
serverless-task-api/
├── template.yaml              # SAM Infrastructure as Code
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI (test + lint)
├── src/
│   ├── handlers/
│   │   ├── create_task.py     # POST /tasks
│   │   ├── get_task.py        # GET  /tasks/{taskId}
│   │   ├── list_tasks.py      # GET  /tasks
│   │   ├── update_task.py     # PUT  /tasks/{taskId}
│   │   └── delete_task.py     # DELETE /tasks/{taskId}
│   └── utils/
│       └── helpers.py         # Shared response/validation helpers
└── tests/
    └── test_handlers.py       # Unit tests (mocked DynamoDB)
```

---

## 🚀 Deployment

### Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.12+

### Deploy to AWS

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/serverless-task-api.git
cd serverless-task-api

# 2. Build the SAM application
sam build

# 3. Deploy (guided first-time setup)
sam deploy --guided

# Follow the prompts — SAM will create a samconfig.toml for future deploys.
# Future deploys: sam deploy
```

After deployment, SAM will output your **API Gateway endpoint URL** and an **API Key** (find the key in the AWS console under API Gateway → API Keys).

---

## 🔌 API Reference

All requests require two headers:

| Header | Description |
|---|---|
| `x-api-key` | Your API Gateway API key |
| `X-User-Id` | The user ID (simulates authentication) |

### Endpoints

#### Create a Task
```http
POST /tasks
```
```json
// Request body
{
  "title": "Study AWS SAM",
  "description": "Complete the hands-on lab",
  "status": "TODO",
  "due_date": "2025-12-31"
}

// Response 201
{
  "message": "Task created",
  "task": {
    "userId": "user-123",
    "taskId": "a1b2c3d4-...",
    "title": "Study AWS SAM",
    "status": "TODO",
    "createdAt": "2025-03-11T12:00:00+00:00",
    "updatedAt": "2025-03-11T12:00:00+00:00"
  }
}
```

#### List All Tasks
```http
GET /tasks
GET /tasks?status=TODO
```

#### Get a Task
```http
GET /tasks/{taskId}
```

#### Update a Task
```http
PUT /tasks/{taskId}

// Body — all fields optional, at least one required
{
  "status": "IN_PROGRESS",
  "title": "Updated title"
}
```

#### Delete a Task
```http
DELETE /tasks/{taskId}
```

---

## 🧪 Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 🔐 Security Design

- **API Key authentication** on all routes via API Gateway Usage Plans
- **Least-privilege IAM**: read-only Lambda functions have `DynamoDBReadPolicy`; write functions have `DynamoDBCrudPolicy`
- **No hardcoded credentials**: all AWS access via Lambda execution roles
- **Input validation** on every handler before touching the database
- **User isolation**: DynamoDB partition key (`userId`) ensures users can only access their own tasks

---

## 💡 Interview Talking Points

When walking through this project in an interview, highlight:

1. **Why serverless?** — Zero idle cost, automatic scaling, no patching overhead
2. **Data modeling** — Composite key design (`userId` + `taskId`) enables efficient per-user queries
3. **Security** — One IAM role per function following least-privilege principle
4. **IaC** — SAM template means the entire stack can be torn down and redeployed in minutes
5. **Pagination** — `list_tasks.py` handles DynamoDB's 1MB page limit with a `while` loop
6. **What I'd add in production** — Cognito for real auth, X-Ray for tracing, WAF on API Gateway

---

## 📈 Potential Enhancements

- [ ] Add Amazon Cognito for real JWT-based authentication
- [ ] Integrate AWS X-Ray for distributed tracing
- [ ] Add a `/tasks/{taskId}/complete` convenience endpoint
- [ ] Set up CloudWatch alarms for Lambda error rates
- [ ] Add DynamoDB Streams → Lambda for real-time notifications via SNS

---

## 🛠️ Tech Stack

| Service | Role |
|---|---|
| AWS Lambda (Python 3.12) | Business logic |
| Amazon API Gateway | HTTP routing + auth |
| Amazon DynamoDB | NoSQL data store |
| AWS SAM | Infrastructure as Code |
| GitHub Actions | CI (test + lint on every push) |
