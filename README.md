# LanChi MCP Engine 🚀

LanChi is a high-performance, premium Model Context Protocol (MCP) Server. It bridges the gap between **AgentSkills** (dynamic actions) and **OneContext** (hybrid long-term memory), providing a state-of-the-art ecosystem for AI Agents.

## ✨ Premium Features

- **Hybrid Memory Architecture**: Seamlessly combines **ChromaDB** (Vector) for semantic knowledge and **DuckDB** (SQL) for persistent history and metadata.
- **Dynamic Skill Ecosystem**: Modular, hot-reloadable skills that can be added or updated without server restarts.
- **Pure Python Mind Mapping**: Generate interactive relationship graphs using Pyvis & NetworkX directly on Windows/IDE.
- **Intelligent Context Management**: Automatic summarization and "fact" extraction to optimize token usage and memory retrieval.
- **Enterprise-Grade Security**: API Key authentication for both SSE and JSON-RPC.
- **Real-time Telemetry**: High-fidelity terminal UI (Rich) showing the status of FastAPI, ChromaDB, and DuckDB.

## 🌐 Web Dashboard (Admin UI)

Access the admin interface at: **`http://localhost:45050/ui`**

The Dashboard provides:
- **Real-time Monitoring**: RAM, CPU, and server status.
- **Skill Registry**: Library of currently loaded AI skills.
- **Endpoints**: List of available MCP connection ports.

## 🧰 Specialized Tools (10+ Core & Dynamic)

### 🧠 Knowledge & Context

- `search_context`: Semantic search across unified memory.
- `memorize_info`: Persistent storage for key findings.
- `skill_context_summarizer`: Compress context and extract facts.

### ⚙️ System & Utilities

- `get_current_time`: Precise system time with timezone support.
- `reload_skills`: Hot-reload of all dynamic skills from the `skills/` directory.

### 🧪 Advanced Skills

- `skill_calculator`: Scientific math operations (sqrt, log, sin, etc.).
- `skill_devdocs`: Instant documentation lookup from DevDocs.io.
- `skill_research_assistant`: Automated web research and auto-indexing.
- `skill_time_scheduler`: Timezone conversion, duration calculation, and automated scheduling.
- `skill_mind_mapper`: Pure Python relationship graph generation (HTML).

## 🛠️ Configuration (IDE Connection)

Add the following configuration to your `mcp_config.json`:

```json
{
  "mcpServers": {
    "lanchi": {
      "serverURL": "http://localhost:45050/mcp/rpc",
      "headers": {
        "X-API-KEY": "LANCHI_SECRET_KEY"
      }
    }
  }
}
```

## 🏗️ Project Structure

- `src/`: Core engine source code (API, Context, History, UI).
- `src/static/`: Web Dashboard assets (Glassmorphism).
- `skills/`: Repository of skill interface definitions (YAML/MD).
- `src/plugins/`: Repository of skill execution logic (Python).
- `db/`: Persistent storage for ChromaDB & DuckDB.

## 🚀 Running LanChi

```bash
uv run lanchi
```

---

> [!IMPORTANT]
> LanChi is optimized for **Windows 11** and **Python 3.12+**. Ensure `uv` is installed for the best experience.

Developed by **Zane Authors** - Empowering the next generation of AI Agents. 🌌
