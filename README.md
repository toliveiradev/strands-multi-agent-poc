# Multi-Agent LLM Orchestration POC

An autonomous multi-agent content orchestration workflow built with the **Strands** framework, featuring containerized on-device inference via **Ollama**.

---

## Workflow Architecture

The pipeline implements a hierarchical supervisor pattern with an integrated evaluator-optimizer feedback loop:

1. **Workflow_Supervisor (Orchestrator):** Analyzes the incoming request, plans execution steps, delegates retrieval, and synthesizes the final draft.
2. **Media_Researcher (Worker):** Fetches internal episode metadata and transcripts via autonomous tool invocation (get_podcast_context).
3. **Brand_Safety_Evaluator (Auditor):** Reviews the generated copy against target demographic profiles and brand safety guidelines, returning structured pass/fail metrics.

---

## Prerequisites

* Docker
* Docker Compose

---

## How to Run

Execute the complete pipeline with a single command:

    docker compose up --build

### Execution Lifecycle

1. Starts the Ollama service in the background.
2. Downloads the llama3.2:3b model to a persistent local Docker volume.
3. Launches the orchestrator container to execute agent reasoning and tool calls.
4. Streams structured JSON telemetry to stdout and outputs the final verified payload.