from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http import StreamableHTTPServerTransport
import mcp.types as types
from src.skills import skill_manager
from src.context import context_manager
import uvicorn
from . import LCNotification

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lanchi")

# 1. Initialize MCP Server
server = Server("LanChi")

def make_tool(name: str, description: str, input_schema: dict) -> types.Tool:
    """Helper to create a fully-compliant MCP Tool with all required non-null fields."""
    return types.Tool(
        name=name,
        title=name.replace("_", " ").title(),
        description=description,
        inputSchema=input_schema,
        outputSchema=None,
        annotations=None,
        icons=None,
        meta=None,
        execution=None,
    )

# 2. Define Tools
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    core_tools = [
        make_tool(
            name="search_context",
            description="Search the OneContext unified memory for relevant information.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "project_id": {"type": "string", "default": "default"},
                },
                "required": ["query", "project_id"],
            },
        ),
        make_tool(
            name="memorize_info",
            description="Add information to the OneContext unified memory.",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "project_id": {"type": "string", "default": "default"},
                },
                "required": ["text", "project_id"],
            },
        ),
        make_tool(
            name="reload_skills",
            description="Reload all dynamic skills from the 'skills/' directory.",
            input_schema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        make_tool(
            name="get_current_time",
            description="Get the current system time in a specific timezone.",
            input_schema={
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "Timezone name (e.g., 'Asia/Ho_Chi_Minh', 'UTC')", "default": "Asia/Ho_Chi_Minh"},
                },
                "required": [],
            },
        ),
    ]
    
    dynamic_skills = []
    for skill in skill_manager.list_loaded_skills():
        props = skill['parameters'].copy()
        props["project_id"] = {"type": "string", "default": "default"}
        dynamic_skills.append(
            make_tool(
                name=f"skill_{skill['name']}",
                description=skill['description'],
                input_schema={
                    "type": "object",
                    "properties": props,
                    "required": (list(skill['parameters'].keys()) if skill['parameters'] else []) + ["project_id"],
                },
            )
        )
    
    return core_tools + dynamic_skills

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent]:
    arguments = arguments or {}
    project_id = arguments.get("project_id", "default")
    
    # Log the incoming "user" request (including project_id)
    await context_manager.log_chat(role="user", content=f"Call tool '{name}' with args: {arguments}", project_id=project_id)
    
    result_data = ""
    # Handle OneContext core tools
    if name == "search_context":
        query = arguments.get("query")
        result_data = await context_manager.query(query, project_id=project_id)
    
    elif name == "memorize_info":
        text = arguments.get("text")
        await context_manager.add_context(text, project_id=project_id)
        result_data = f"Information memorized successfully for project '{project_id}'."
    
    elif name == "reload_skills":
        skill_manager.reload_skills()
        result_data = "All skills have been reloaded successfully."
    
    elif name == "get_current_time":
        import datetime
        try:
            import pytz
            tz_name = arguments.get("timezone", "Asia/Ho_Chi_Minh")
            tz = pytz.timezone(tz_name)
            now = datetime.datetime.now(tz)
            result_data = now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        except Exception:
            result_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Handle Dynamic AgentSkills
    elif name.startswith("skill_"):
        skill_name = name.replace("skill_", "")
        result_data = await skill_manager.execute_skill(skill_name, **arguments)
    
    else:
        raise ValueError(f"Unknown tool: {name}")

    # Log the response back to history for the specific project
    await context_manager.log_chat(role="assistant", content=str(result_data), project_id=project_id)
    
    # Handle Image Response
    if isinstance(result_data, dict) and result_data.get("type") == "image":
        return [
            types.ImageContent(
                type="image",
                data=result_data["data"],
                mimeType=f"image/{result_data['format']}"
            )
        ]
    
    return [types.TextContent(type="text", text=str(result_data))]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Kết nối cơ sở dữ liệu
    from src.history import history_db
    try:
        history_db.connect()
        logger.info("Connected to DuckDB history database.")
    except Exception as e:
        logger.error(f"Failed to connect to DuckDB: {e}")

    # Hiển thị banner (ONLINE)
    skills = [s['name'] for s in skill_manager.list_loaded_skills()]
    LCNotification.startup_lanchi(api_status="[bold green]ONLINE[/bold green]", test_tools=skills)
    
    yield
    
    # Shutdown: Ngắt kết nối cơ sở dữ liệu
    from src.history import history_db
    from src.context import context_manager
    history_db.close()
    context_manager.close()
    logger.info("Shutdown complete.")

# 3. Initialize FastAPI
app = FastAPI(title="LanChi MCP Server", lifespan=lifespan)

from fastapi.staticfiles import StaticFiles
import os

# Create static directory if not exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Mount UI
app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="ui")

@app.get("/mcp/status")
async def get_mcp_status():
    """Endpoint for the Web UI to fetch real-time stats."""
    import psutil
    loaded_skills = skill_manager.list_loaded_skills()
    return {
        "server": "LanChi Engine",
        "version": "1.0.0",
        "status": "online",
        "ram": f"{psutil.virtual_memory().percent}%",
        "cpu": f"{psutil.cpu_percent()}%",
        "skills": loaded_skills,
        "endpoints": {
            "streamable": "/mcp",
            "sse": "/mcp/sse",
            "rpc": "/mcp/rpc"
        }
    }


# 4. Setup SSE Transport
sse = SseServerTransport("/mcp/messages")

@app.get("/mcp/sse")
async def handle_sse(request: Request):
    # API Key check for SSE
    api_key = request.headers.get("X-API-KEY") or request.headers.get("API_KEY")
    EXPECTED_KEY = "LANCHI_SECRET_KEY"
    
    if api_key != EXPECTED_KEY:
        logger.warning(f"Unauthorized SSE attempt from {request.client.host}")
        return Response(status_code=401, content="Unauthorized")

    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

@app.post("/mcp/messages")
async def handle_messages(request: Request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

@app.get("/")
async def root():
    return {
        "message": "LanChi MCP Server is running",
        "endpoints": {
            "streamable_http": "/mcp",
            "sse": "/mcp/sse",
            "json_rpc": "/mcp/rpc"
        }
    }

@app.post("/mcp")
@app.get("/mcp")
async def handle_streamable_http(request: Request):
    """
    StreamableHTTP endpoint - supported by modern IDEs like AWS Kiro.
    """
    # API Key check
    api_key = request.headers.get("X-API-KEY") or request.headers.get("API_KEY")
    EXPECTED_KEY = "LANCHI_SECRET_KEY"
    
    if api_key != EXPECTED_KEY:
        logger.warning(f"Unauthorized StreamableHTTP attempt from {request.client.host}")
        return Response(status_code=401, content="Unauthorized")

    transport = StreamableHTTPServerTransport(
        mcp_session_id=request.headers.get("mcp-session-id"),
        is_json_response_enabled=True
    )
    async with transport.connect() as (read_stream, write_stream, _get_response):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )
        return await _get_response(request.scope, request.receive, request._send)

@app.post("/mcp/rpc")
async def handle_rpc(request: Request):
    """
    Direct JSON-RPC endpoint with API KEY security.
    """
    # Simple API Key check
    api_key = request.headers.get("X-API-KEY") or request.headers.get("API_KEY")
    EXPECTED_KEY = "LANCHI_SECRET_KEY" # In production, use os.getenv("LANCHI_API_KEY")
    
    if api_key != EXPECTED_KEY:
        logger.warning(f"Unauthorized access attempt from {request.client.host}")
        return JSONResponse(
            status_code=401,
            content={"error": "Unauthorized: Invalid API Key"}
        )

    try:
        data = await request.json()
        method = data.get("method")
        request_id = data.get("id")
        
        logger.info(f"RPC Request: {method} (id={request_id})")

        # Lifecycle: Initialize
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {"listChanged": False, "subscribe": False},
                        "prompts": {"listChanged": False}
                    },
                    "serverInfo": {"name": "LanChi-Server", "version": "0.1.0"}
                }
            }
        
        # Lifecycle: Initialized notification (no response needed)
        if method == "notifications/initialized":
            logger.info("MCP Client initialized.")
            return Response(status_code=200)
            
        # Lifecycle: Cancelled notification
        if method == "notifications/cancelled":
            logger.info(f"MCP Request cancelled: {data.get('params', {}).get('requestId')}")
            return Response(status_code=200)

        # Lifecycle: Resource/Tool/Prompt changes (notifications)
        if method in ["notifications/resources/list_changed", "notifications/tools/list_changed", "notifications/prompts/list_changed"]:
            return Response(status_code=200)

        # Tool Listing
        if method == "tools/list":
            tools = await handle_list_tools()
            return {
                "jsonrpc": "2.0", 
                "id": request_id, 
                "result": {"tools": [t.model_dump(exclude_none=True) for t in tools]}
            }
        
        # Tool Execution
        if method == "tools/call":
            params = data.get("params", {})
            name = params.get("name")
            args = params.get("arguments")
            try:
                result = await handle_call_tool(name, args)
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id, 
                    "result": {
                        "content": [c.model_dump(exclude_none=True) for c in result]
                    }
                }
            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32603, "message": str(e)}
                }
        
        # Method not found
        logger.warning(f"Unknown RPC method: {method}")
        return {
            "jsonrpc": "2.0", 
            "id": request_id, 
            "error": {"code": -32601, "message": f"Method '{method}' not found"}
        }
    except Exception as e:
        logger.error(f"RPC endpoint error: {e}")
        return JSONResponse(
            status_code=500,
            content={"jsonrpc": "2.0", "error": {"code": -32000, "message": "Internal server error"}}
        )

@app.get("/health")
async def health_check():
    # Lấy danh sách skill thực tế để báo cáo
    loaded_skills = skill_manager.list_loaded_skills()
    return {
        "status": "online",
        "version": "1.0.0",
        "components": {
            "agent_skills": len(loaded_skills),
            "context_manager": "connected",
            "mcp_server": server.name
        }
    }

def run_server():
    """Entry point for the project script."""
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=45050, reload=True)

if __name__ == "__main__":
    import sys
    if "--stdio" in sys.argv:
        from mcp.server.stdio import stdio_server
        async def run_stdio():
            async with stdio_server() as (read_stream, write_stream):
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options()
                )
        import asyncio
        asyncio.run(run_stdio())
    else:
        run_server()
