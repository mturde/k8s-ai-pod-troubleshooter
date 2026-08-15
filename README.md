# 🚀 Kubernetes AI Pod Troubleshooter

> **AI-powered Kubernetes troubleshooting** with local LLM. Analyze pod failures automatically using kubectl logs, events, and descriptions—no cloud APIs needed.

<div align="center">

![Kubernetes](https://img.shields.io/badge/Kubernetes-1.27+-326CE5?logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-FF6B6B)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

## 🎯 Overview

Troubleshoot Kubernetes pod failures with **local AI** (no cloud APIs):
- 🔍 Collect pod logs & events
- 🔐 Redact sensitive data
- 🧠 Analyze with local LLM
- 📊 Get JSON report with root cause & recommendations

## 🏗️ Architecture

```
Kubernetes Pod (Failed)
    ↓ kubectl
┌─────────────────────┐
├─ Pod Describe      │
├─ Logs (current)    │
├─ Logs (previous)   │
└─ Events            │
    ↓ Sanitize
   🔐 Remove secrets
    ↓ Analyze
   🧠 Ollama LLM
    ↓
📋 JSON Report
(Status, Cause, Recommendations)
```

## ✨ Features

- ✅ Collect pod logs, events, description
- ✅ Auto redact credentials
- ✅ Local LLM analysis (Ollama)
- ✅ JSON structured output
- ✅ Read-only (safe)

## 📋 Requirements

- 🐳 Docker (v29+)
- ☸️ Kubernetes (v1.27+)
- 🐍 Python (3.8+)
- 🦙 Ollama (v0.32+)
- 🌀 kind (v0.32+)

## 🚀 Quick Start

**1. Create Kubernetes cluster:**
```bash
kind create cluster --name ai-lab
```

**2. Setup Ollama:**
```bash
ollama serve &
ollama pull gemma3:4b
```

**3. Install Python deps:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**4. Run analysis:**
```bash
python analyzer.py --pod <POD_NAME> --namespace <NAMESPACE>
```

**Example:**
```bash
kubectl apply -f manifests/broken-pod.yaml
python analyzer.py --pod broken-app --namespace default
```

## 📊 Test Results

**Environment Setup (2026-08-15):**

| Component | Version | Status |
|-----------|---------|--------|
| Docker | 29.6.2 | ✅ |
| kubectl | 1.27 | ✅ |
| kind | 0.32.0 | ✅ |
| Python | 3.13.5 | ✅ |
| Ollama | 0.32.9 | ✅ |

**Live Example - Redis Connection Error:**

```json
{
  "status": "Failed",
  "summary": "Pod is crashing due to Redis connection error",
  "likely_cause": "Application cannot connect to Redis at redis:6379",
  "evidence": [
    "Image: busybox:1.36",
    "State: CrashLoopBackOff",
    "Exit Code: 1",
    "Logs: ERROR: Cannot connect to Redis at redis:6379"
  ],
  "recommended_checks": [
    "Verify Redis service is running",
    "Check network connectivity to redis:6379",
    "Inspect pod logs for error details"
  ],
  "confidence": "high"
}
```

**Metrics:**
- ⏱️ Analysis time: ~10-30s
- 🎯 Accuracy: High for common failures
- 🔐 Privacy: 100% local (no cloud)
- 💰 Cost: $0

## 🔒 Security

Automatically redacts: passwords, API keys, tokens, connection strings

##  Project Structure

```
k8s-ai-pod-troubleshooter/
├── analyzer.py                 # Main script
├── requirements.txt            # Dependencies
├── README.md
├── manifests/
│   └── broken-pod.yaml        # Test pod example
└── examples/
```

## 📄 License

MIT