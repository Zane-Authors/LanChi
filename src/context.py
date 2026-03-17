import chromadb
from chromadb.config import Settings
import logging
from typing import List, Optional
import os
from src.history import history_db

logger = logging.getLogger("lanchi.context")

class ContextManager:
    """
    Manages unified context and memory.
    - ChromaDB (Vector) for dynamic knowledge.
    - DuckDB (SQL) for persistent chat history and metadata.
    """
    def __init__(self, db_path: str = "./chroma_db"):
        self.db_path = db_path
        self.client = None
        self.write_lock = None
        self.knowledge_collection = None

    def _ensure_connected(self):
        if self.client is None:
            import asyncio
            os.makedirs(self.db_path, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.write_lock = asyncio.Lock()
            # Collection for general knowledge/facts (Vector Search)
            self.knowledge_collection = self.client.get_or_create_collection(
                name="lanchi_knowledge",
                metadata={"hnsw:space": "cosine"}
            )

    def close(self):
        """Clean up resources."""
        if self.client:
            # ChromaDB's PersistentClient doesn't always have a close() method in all versions,
            # but we can clear references.
            self.client = None
            self.knowledge_collection = None
            logger.info("ChromaDB references cleared.")

    async def add_context(self, text: str, project_id: str = "default", metadata: dict = None):
        """Add knowledge to the vector collection."""
        self._ensure_connected()
        logger.info(f"Adding to knowledge [Vector: {project_id}]: {text[:50]}...")
        doc_id = str(hash(text + project_id))
        
        meta = metadata or {}
        meta["project_id"] = project_id
        
        async with self.write_lock:
            self.knowledge_collection.add(
                documents=[text],
                metadatas=[meta],
                ids=[doc_id]
            )

    async def log_chat(self, role: str, content: str, project_id: str = "default", session_id: str = "default"):
        """Delegate chat logging to DuckDB."""
        await history_db.log_chat(role, content, project_id, session_id)

    async def query(self, query_text: str, project_id: str = "default", n_results: int = 3, include_history: bool = True) -> str:
        """Query across Vector Knowledge and DuckDB History."""
        self._ensure_connected()
        logger.info(f"Unified query for: {query_text} [Project: {project_id}]")
        
        # 1. Search Vector Knowledge (ChromaDB)
        k_results = self.knowledge_collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"project_id": project_id}
        )
        knowledge_texts = k_results['documents'][0] if k_results['documents'] else []
        
        # 2. Search History (DuckDB - SQL Text Search)
        history_texts = []
        if include_history:
            history_texts = history_db.search_history(project_id, query_text)

        if not knowledge_texts and not history_texts:
            return f"No relevant context found for project '{project_id}'."
        
        output = [f"## Unified Context: {project_id}"]
        if knowledge_texts:
            output.append("### Relevant Knowledge (Vector):\n" + "\n---\n".join(knowledge_texts))
        if history_texts:
            output.append("### Relevant Past Conversations (SQL):\n" + "\n---\n".join(history_texts))
            
        return "\n\n".join(output)

# Determine project root and use absolute path for DB
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
context_manager = ContextManager(db_path=os.path.join(PROJECT_ROOT, "db", "chroma_db"))
