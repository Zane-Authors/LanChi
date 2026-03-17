# LanChi MCP Engine 🚀

LanChi is a high-performance, premium Model Context Protocol (MCP) Server. It bridges the gap between **AgentSkills** (dynamic actions) and **OneContext** (hybrid long-term memory), providing a state-of-the-art ecosystem for AI Agents.

## ✨ Premium Features

- **Hybrid Memory Architecture**: Seamlessly combines **ChromaDB** (Vector) for semantic knowledge and **DuckDB** (SQL) for persistent history and metadata.
- **Dynamic Skill Ecosystem**: Modular, hot-reloadable skills that can be added or updated without server restarts.
- **Pure Python Mind Mapping**: Generate interactive relationship graphs using Pyvis & NetworkX trực tiếp trên Windows/IDE.
- **Intelligent Context Management**: Automatic summarization and "fact" extraction to optimize token usage and memory retrieval.
- **Enterprise-Grade Security**: API Key authentication cho cả SSE và JSON-RPC.
- **Real-time Telemetry**: High-fidelity terminal UI (Rich) hiển thị trạng thái của FastAPI, ChromaDB, và DuckDB.

## 🧰 Specialized Tools (10+ Core & Dynamic)

### 🧠 Knowledge & Context

- `search_context`: Semantic search across unified memory.
- `memorize_info`: Persistent storage for key findings.
- `skill_context_summarizer`: Nén ngữ cảnh, trích xuất sự thật (Facts).

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

Thêm cấu hình sau vào `mcp_config.json` của bạn:

```json
{
  "mcpServers": {
    "lanchi": {
      "serverURL": "http://localhost:5050/mcp/rpc",
      "headers": {
        "X-API-KEY": "LANCHI_SECRET_KEY"
      }
    }
  }
}
```

## 🏗️ Project Structure

- `src/`: Core engine source code (API, Context, History, UI).
- `skills/`: A modular repository of agent capabilities (YAML + Python logic).
- `db/`: Persistent storage for ChromaDB & DuckDB.

## 🚀 Running LanChi

```bash
uv run uvicorn src.main:app --port 5050 --reload
```

---

> [!IMPORTANT]
> LanChi được tối ưu hóa cho **Windows 11** và **Python 3.12+**. Đảm bảo đã cài đặt `uv` để có trải nghiệm tốt nhất.

Developed by **Zane Authors** - Empowering the next generation of AI Agents. 🌌
