from src.history import history_db
import httpx
import json

async def execute(action="read", content="", agent_name="AI-Agent", project_id="default", **kwargs):
    """
    Agent-to-Agent communication bridge.
    """
    if action == "send":
        if not content:
            return "❌ Error: Content cannot be empty when sending a message."
        
        # Log to DuckDB
        # agent_id can be inferred or unique per session
        agent_id = f"{agent_name}-{kwargs.get('session_id', 'global')}"
        res = await history_db.log_agent_message(agent_id, agent_name, content, project_id)
        
        # Notify the UI (via internal broadcast if available, or just log for now)
        # In a real collaborative environment, we might push to an external webhook or SSE
        
        return f"✅ Message sent as [{agent_name}]: '{content}' (ID: {res['id']})"
    
    # default action is "read"
    history = history_db.get_agent_chat_history(project_id, limit=15)
    
    if not history:
        return f"ℹ️ The Group Chat for project [{project_id}] is empty. Be the first to start the conversation!"
    
    output = f"🗨️ [Project: {project_id.upper()}] Recent Activity:\n"
    for msg in reversed(history):  # Show oldest first for natural flow
        output += f"- [{msg['timestamp'][11:16]}] {msg['agent_name']}: {msg['content']}\n"
    
    return output
