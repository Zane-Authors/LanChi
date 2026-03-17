import duckdb
import os
import datetime
import logging

logger = logging.getLogger("lanchi.history")

class HistoryManager:
    """
    Manages persistent chat history and project metadata using DuckDB.
    Replaces RAM-based SQLite with a lightweight, file-based SQL database.
    """
    def __init__(self, db_path: str = "lanchi_history.db"):
        self.db_path = db_path
        self.conn = None
        self.write_lock = None

    def connect(self):
        """Initialize DuckDB connection (persistent file)."""
        if self.conn is None:
            self.conn = duckdb.connect(self.db_path)
            import asyncio
            self.write_lock = asyncio.Lock()
            self._init_tables()
        return self

    def close(self):
        """Close the DuckDB connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("DuckDB connection closed.")

    def _init_tables(self):
        """Create necessary tables if they don't exist."""
        if not self.conn: return
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id VARCHAR PRIMARY KEY,
                project_id VARCHAR,
                session_id VARCHAR,
                role VARCHAR,
                content TEXT,
                timestamp TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id VARCHAR PRIMARY KEY,
                name VARCHAR,
                created_at TIMESTAMP,
                metadata JSON
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_group_chat (
                id VARCHAR PRIMARY KEY,
                agent_id VARCHAR,
                agent_name VARCHAR,
                content TEXT,
                project_id VARCHAR,
                timestamp TIMESTAMP
            )
        """)
        logger.info(f"DuckDB initialized at {self.db_path}")

    async def log_agent_message(self, agent_id: str, agent_name: str, content: str, project_id: str = "default"):
        """Logs a message sent from one agent to the group chat."""
        if not self.conn: self.connect()
        import uuid
        message_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now()
        
        async with self.write_lock:
            self.conn.execute("""
                INSERT INTO agent_group_chat (id, agent_id, agent_name, content, project_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (message_id, agent_id, agent_name, content, project_id, timestamp))
            logger.info(f"Agent message logged: [{agent_name}] in [{project_id}]")
        return {"id": message_id, "timestamp": timestamp.isoformat()}

    def get_agent_chat_history(self, project_id: str = None, limit: int = 20):
        """Retrieves recent group chat history. If project_id is None, returns messages from all projects."""
        if not self.conn: self.connect()
        
        if project_id:
            query = """
                SELECT agent_name, content, timestamp, agent_id, project_id
                FROM agent_group_chat 
                WHERE project_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
            params = (project_id, limit)
        else:
            query = """
                SELECT agent_name, content, timestamp, agent_id, project_id
                FROM agent_group_chat 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
            params = (limit,)

        result = self.conn.execute(query, params).fetchall()
        
        return [
            {
                "agent_name": r[0], 
                "content": r[1], 
                "timestamp": r[2].isoformat(), 
                "agent_id": r[3],
                "project_id": r[4]
            } for r in result
        ]

    async def log_chat(self, role: str, content: str, project_id: str = "default", session_id: str = "default"):
        if not self.conn: self.connect()
        import uuid
        message_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now()
        
        async with self.write_lock:
            self.conn.execute("""
                INSERT INTO chat_history (id, project_id, session_id, role, content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (message_id, project_id, session_id, role, content, timestamp))
            logger.info(f"Chat logged to DuckDB [Project: {project_id}]")

    def get_recent_history(self, project_id: str, limit: int = 10):
        if not self.conn: self.connect()
        result = self.conn.execute("""
            SELECT role, content, timestamp 
            FROM chat_history 
            WHERE project_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (project_id, limit)).fetchall()
        
        return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in result]

    def search_history(self, project_id: str, query: str, limit: int = 5):
        """Full-text search in chat history using DuckDB."""
        if not self.conn: self.connect()
        result = self.conn.execute("""
            SELECT role, content 
            FROM chat_history 
            WHERE project_id = ? AND content ILIKE ?
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (project_id, f"%{query}%", limit)).fetchall()
        
        return [f"{r[0]}: {r[1]}" for r in result]

# Determine project root based on this file's location
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(PROJECT_ROOT, "db")
os.makedirs(DB_DIR, exist_ok=True)

# Initialize global history manager instance (doesn't connect yet)
history_db = HistoryManager(db_path=os.path.join(DB_DIR, "lanchi_history.duckdb"))
