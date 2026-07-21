# MCP Filesystem Agent

A Gradio-based AI Filesystem Assistant that uses a Large Language Model (LLM) and the Model Context Protocol (MCP) Filesystem Server to perform file operations within a secure sandbox directory.

---

## Features

- Natural language file operations
- MCP-based filesystem access
- Read files
- Create files
- Edit files
- Search files
- Summarize files
- Summarize multiple files
- Compare files
- Tool execution tracing
- Secure sandbox enforcement
- Overwrite confirmation for edits
- Tool call logging

---

## Architecture

```text
                      User
                       │
                       ▼
                Gradio Chat UI
                    (app.py)
                       │ Natural Language Request
                       ▼
                Agent Orchestrator
              (agent/orchestrator.py)
               |  ────────────────  |                  
               ▼                    ▼
            GPT-OSS LLM      MCP Client
           (llm_client.py)  (mcp_client.py)
               │                    |
               | Tool Decision      │ Tool Execution
               ▼                    ▼
         JSON Tool Call   MCP ClientSession
                                    │
                                    ▼
                           Filesystem MCP Server
                  (@modelcontextprotocol/server-filesystem)
                                    │
                                    ▼
                            Sandbox Directory
                                    │
                       ┌────────────┼────────────┐
                       ▼            ▼            ▼
                     .txt         .csv         .py
                     Files        Files       Files

```

---

## Project Structure

```text
filesystem_agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── agent/
│   ├── __init__.py
│   ├── llm_client.py
│   ├── mcp_client.py
│   └── orchestrator.py
│
├── sandbox/
│   ├── notes.txt
│   ├── report.txt
│   ├── meeting_notes.txt
│   ├── sales.csv
│   ├── test.txt
│   └── ...
│
├── logs/
│   └── tool_calls.log
│
└── tests/
    ├── test_mcp.py
    ├── test_write.py
    └── test_search.py

```

---

## Setup

### 1. Clone Repository

```bash
git clone <repo-url>
cd filesystem_agent
```

---

### 2. Create and Activate a Virtual Environment

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

After activation, the terminal prompt should display:

```text
(.venv)
```

---

## Environment Variables

Create a `.env` file:

```env
API_URL=http://YOUR_ENDPOINT/v1/chat/completions
API_KEY=YOUR_API_KEY
MODEL=openai/gpt-oss-20b
ALLOWED_DIRECTORY=sandbox
```

---

## MCP Filesystem Server

This project uses the official MCP Filesystem Server.

Install automatically through:

```bash
npx -y @modelcontextprotocol/server-filesystem sandbox
```

The MCP server is restricted to the sandbox directory and cannot access files outside it.

---

## Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

---

## Example Prompts

### List Files

```text
Display folder contents
```

```text
What's in this folder?
```

---

### Read Files

```text
Read notes.txt
```

---

### Create Files

```text
Create hello.py with a hello world program
```

---

### Edit Files

```text
Rewrite test.txt to hello world
```

The assistant will ask for confirmation before overwriting:

```text
This will overwrite test.txt.
Reply YES to continue.
```

---

### Search Files

```text
Find all .csv files
```

---

### Summarize Files

```text
Read report.txt and summarize it
```

---

### Summarize Entire Directory

```text
Summarize all text files in the sandbox directory
```

---

### Compare Files

```text
Compare notes.txt and report.txt
```

---

## Security Features

### Sandbox Restriction

Access outside the sandbox directory is denied.

Example:

```text
Read /etc/passwd
```

Output:

```text
Access denied: outside sandbox directory
```

---

### Overwrite Confirmation

Any file overwrite requires explicit user confirmation:

```text
Reply YES to continue.
```

---

## Tool Trace Example

```text
TOOL TRACE

MCP: read_text_file('report.txt')
summarize_content()

RESULT

<summary>
```

This provides visibility into the agent's actions.

---

## Logging

All tool calls are recorded in:

```text
logs/tool_calls.log
```

Captured details:

- Timestamp
- Tool Name
- Arguments
- Result

---

## Supported Operations

| Operation | Supported |
|------------|------------|
| Read File | ✅ |
| Create File | ✅ |
| Edit File | ✅ |
| Search Files | ✅ |
| List Directory | ✅ |
| Summarize File | ✅ |
| Summarize All Files | ✅ |
| Compare Files | ✅ |
| Delete File | Not Implemented |

---

## Error Handling

Examples:

Missing file:

```text
File not found
```

Unauthorized path:

```text
Access denied: outside sandbox directory
```

Unsupported delete:

```text
File deletion is not implemented.
```

---

## Learning Outcomes

- MCP architecture
- MCP Filesystem Server integration
- Tool-calling orchestration
- Async Python workflows
- Gradio UI development
- Sandbox security enforcement
- AI agent design patterns

---

