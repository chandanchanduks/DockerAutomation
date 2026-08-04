# 🚀 Docker Automation - DevOps Learning Journey

> A complete hands-on DevOps learning project covering Docker, Jenkins, CI/CD, GitHub Webhooks, and Python Automation.

---

# 📌 Project Goal

Build a complete CI/CD pipeline for an Android Automation Framework using

- Python
- Docker
- Docker Compose
- Jenkins
- Git & GitHub
- GitHub Webhooks
- Cloudflare Tunnel

---

# 🏗️ Overall Architecture

```text
                Git Push
                    │
                    ▼
             GitHub Repository
                    │
                 Webhook
                    │
          Cloudflare Quick Tunnel
                    │
          Jenkins Pipeline (8080)
                    │
            docker compose up
                    │
        ┌───────────┴────────────┐
        │                        │
 Device Container         Automation Container
        │                        │
     Flask API             Python Automation
        │                        │
        └────────────┬───────────┘
                     │
               Test Reports
                     │
                docker cp
                     │
             Jenkins Artifacts
```

---

# 📚 Topics Covered

## ✅ Linux

Learned

- Linux File System
- Users & Groups
- Permissions
- Shell Scripting
- Process Management
- Environment Variables

---

# ✅ Git

## Commands

```bash
git init
git clone
git add .
git commit -m ""
git push
git pull
git status
git log
git branch
git checkout
git reset --soft
git reset --mixed
git reset --hard
git rebase
git stash
```

## Authentication

Configured GitHub Personal Access Token.

---

# ✅ Docker

## Concepts

- Images
- Containers
- Dockerfile
- Layers
- Build Cache
- Bind Mounts
- Named Volumes
- Networks
- Docker Compose

---

## Docker Commands

```bash
docker build
docker run
docker ps
docker images
docker stop
docker start
docker restart
docker rm
docker exec
docker logs
docker inspect
docker cp
```

---

## Docker Compose Commands

```bash
docker compose up
docker compose up --build
docker compose down
docker compose logs
docker compose ps
docker compose ps -aq
```

---

# ✅ Jenkins

## Custom Jenkins Image

Built using

```bash
docker build -t my-jenkins:v3 .
```

---

## Jenkins Container

```bash
docker run -d \
--name jenkins \
-p 8080:8080 \
-p 50000:50000 \
-v ~/jenkins_home:/var/jenkins_home \
-v /var/run/docker.sock:/var/run/docker.sock \
my-jenkins:v3
```

---

## Daily Jenkins Commands

Start

```bash
docker start jenkins
```

Stop

```bash
docker stop jenkins
```

Restart

```bash
docker restart jenkins
```

Logs

```bash
docker logs -f jenkins
```

Enter Container

```bash
docker exec -it jenkins bash
```

---

# ✅ Jenkins Pipeline

Learned

- Declarative Pipeline
- agent
- stages
- steps
- environment
- parameters
- script{}
- post{}
- archiveArtifacts
- checkout scm

---

# ✅ Groovy

## Variables

```groovy
def name="Chandan"
```

---

## String Interpolation

```groovy
echo "${name}"
```

---

## If Else

```groovy
if(condition){

}
else{

}
```

---

## For Loop

```groovy
for(int i=0;i<5;i++){

}
```

---

## each Loop

```groovy
list.each{

}
```

---

## Maps

```groovy
def device=[
name:"Pixel",
battery:82
]
```

---

## Environment Variables

```groovy
env.WORKSPACE

env.BUILD_NUMBER

env.JOB_NAME
```

---

## Running Shell Commands

```groovy
sh "pwd"
```

Return Output

```groovy
sh(
script:"pwd",
returnStdout:true
)
```

Return Status

```groovy
sh(
script:"ls",
returnStatus:true
)
```

---

# ✅ Jenkins Build Parameters

## String Parameter

```groovy
string(...)
```

---

## Boolean Parameter

```groovy
booleanParam(...)
```

---

## Choice Parameter

```groovy
choice(...)
```

---

Access

```groovy
params.TEST_SUITE
```

---

# ✅ Current Pipeline Flow

```text
Checkout

↓

Build Images (Optional)

↓

docker compose up

↓

Wait For Automation

↓

Container Logs

↓

Copy Reports

↓

Archive Reports

↓

Cleanup (Optional)
```

---

# ✅ Docker Report Collection

Current Method

```bash
docker cp <container_id>:/automation/reports/. automation_reports/
```

Reason

Container names can change.

Container IDs are always unique and reliable.

---

# ✅ Jenkins Artifacts

Archive

```groovy
archiveArtifacts(
artifacts:'automation_reports/**',
fingerprint:true
)
```

View

```text
Build

↓

Artifacts
```

---

# ✅ GitHub Webhook

Flow

```text
Git Push

↓

GitHub

↓

Webhook

↓

Cloudflare Tunnel

↓

Jenkins

↓

Pipeline
```

---

# ✅ Cloudflare Tunnel

Start Tunnel

```bash
cloudflared tunnel --url http://localhost:8080
```

Example URL

```text
https://xxxxx.trycloudflare.com
```

Webhook URL

```text
https://xxxxx.trycloudflare.com/github-webhook/
```

> Quick Tunnel changes every restart.

---

# ✅ Docker Automation Project Structure

```text
DockerAutomation/

│
├── Automation/
│      ├── Dockerfile
│      ├── app.py
│      └── requirements.txt
│
├── Device/
│      ├── Dockerfile
│      ├── app.py
│      └── requirements.txt
│
├── automation_reports/
│
├── compose.yaml
│
├── Jenkinsfile
│
└── README.md
```

---

# ✅ Important Commands

## Docker

```bash
docker compose up --build -d
```

```bash
docker compose down
```

```bash
docker compose logs
```

```bash
docker compose ps
```

```bash
docker compose ps -aq automation
```

---

## Jenkins

```bash
docker start jenkins
```

```bash
docker logs -f jenkins
```

```bash
docker exec -it jenkins bash
```

---

## Cloudflare

```bash
cloudflared tunnel --url http://localhost:8080
```

---

# 🎯 Learning Progress

- ✅ Linux
- ✅ Git
- ✅ GitHub
- ✅ Docker
- ✅ Docker Compose
- ✅ Jenkins Installation
- ✅ Jenkins Pipelines
- ✅ Groovy Basics
- ✅ Docker Integration
- ✅ GitHub Webhooks
- ✅ Cloudflare Tunnel
- ✅ Jenkins Parameters
- ✅ Report Collection
- ✅ Artifact Archiving

---

# 📖 Upcoming Topics

- ⏳ Python argparse
- ⏳ Dynamic Test Suite Execution
- ⏳ Jenkins Credentials
- ⏳ Parallel Stages
- ⏳ Shared Libraries
- ⏳ Multi-Branch Pipelines
- ⏳ Docker Registry
- ⏳ Kubernetes
- ⏳ Helm
- ⏳ GitHub Actions
- ⏳ AWS CI/CD

---

# 📝 Notes

This document will be updated continuously as new DevOps concepts are learned.