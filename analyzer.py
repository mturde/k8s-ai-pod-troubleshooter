import argparse
import json
import re
import subprocess

import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:4b"


def run_kubectl(args):
    command = ["kubectl"] + args

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=20
    )

    if result.returncode != 0:
        return f"Command failed: {result.stderr.strip()}"

    return result.stdout.strip()


def collect_pod_data(namespace, pod):
    describe = run_kubectl([
        "describe",
        "pod",
        pod,
        "-n",
        namespace
    ])

    logs = run_kubectl([
        "logs",
        pod,
        "-n",
        namespace,
        "--tail=200"
    ])

    previous_logs = run_kubectl([
        "logs",
        pod,
        "-n",
        namespace,
        "--previous",
        "--tail=200"
    ])

    events = run_kubectl([
        "events",
        "-n",
        namespace,
        "--for",
        f"pod/{pod}"
    ])

    return {
        "describe": describe,
        "logs": logs,
        "previous_logs": previous_logs,
        "events": events
    }


def redact_secrets(text):
    patterns = [
        (
            r'(?i)(password|passwd|token|secret|api[_-]?key)\s*[:=]\s*[^\s,;]+',
            r'\1=<REDACTED>'
        ),
        (
            r'(?i)Bearer\s+[A-Za-z0-9\-._~+/]+=*',
            'Bearer <REDACTED>'
        )
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    return text


def sanitize_data(data):
    return {
        key: redact_secrets(value)
        for key, value in data.items()
    }


def analyze_with_ai(data):
    prompt = f"""
You are a Kubernetes troubleshooting assistant.

Analyze the Kubernetes Pod information below.

Rules:
- Use only the evidence provided.
- Do not invent missing information.
- Do not recommend destructive actions.
- Clearly separate evidence from assumptions.
- If the root cause is uncertain, say so.

Return JSON with exactly these fields:

{{
  "status": "",
  "summary": "",
  "likely_cause": "",
  "evidence": [],
  "recommended_checks": [],
  "confidence": "low|medium|high"
}}

KUBERNETES DESCRIBE:
{data["describe"]}

CURRENT LOGS:
{data["logs"]}

PREVIOUS LOGS:
{data["previous_logs"]}

EVENTS:
{data["events"]}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "format": "json"
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return json.loads(
        result["message"]["content"]
    )


def main():
    parser = argparse.ArgumentParser(
        description="AI Kubernetes Pod Troubleshooter"
    )

    parser.add_argument(
        "--pod",
        required=True,
        help="Kubernetes Pod name"
    )

    parser.add_argument(
        "--namespace",
        default="default",
        help="Kubernetes namespace"
    )

    args = parser.parse_args()

    print(
        f"Collecting Kubernetes data for "
        f"{args.namespace}/{args.pod}..."
    )

    data = collect_pod_data(
        args.namespace,
        args.pod
    )

    sanitized_data = sanitize_data(data)

    print("Analyzing Pod with local AI...")

    analysis = analyze_with_ai(
        sanitized_data
    )

    print("\n--- AI Kubernetes Analysis ---\n")

    print(
        json.dumps(
            analysis,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()