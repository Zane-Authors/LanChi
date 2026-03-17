import asyncio
import os
from src.context import context_manager

async def save_lanchi_specs():
    project_summary = """
    Dự án: LanChi (MCP Server) - Phiên bản Cao cấp
    Kiến trúc Hệ thống: 
    - Bridge Layer: 'src/bridge.py' (Stdio <-> HTTP 5050 Proxy) tối ưu cho Windows.
    - API Layer: FastAPI (Uvicorn) chạy tại cổng 5050.
    - Memory Layer (Hybrid): 
        * ChromaDB: Vector Knowledge lưu tại 'db/chroma_db'.
        * DuckDB: Chat History & Metadata lưu tại 'db/lanchi_history.duckdb'.
    - UI Layer: 'src/LCNotification.py' sử dụng thư viện Rich cho trải nghiệm terminal cao cấp.
    
    Tính năng cốt lõi:
    1. Dynamic Skill Loading: Tự động tải từ 'skills/'.
    2. OneContext Memory: Bộ nhớ dài hạn đa nền tảng (Vector + SQL).
    3. Project Isolation: Phân tách dữ liệu theo 'project_id'.
    4. Persistent Bridge: Giữ kết nối LLM bền vững không cần restart server thường xuyên.
    
    Thư viện chính: mcp, fastapi, chromadb, duckdb, rich, httpx.
    """
    
    print("Memorizing LanChi project specs into OneContext...")
    
    # Ghi nhớ vào hệ thống với project_id là 'lanchi_meta'
    await context_manager.add_context(
        text=project_summary,
        project_id="lanchi_internal",
        metadata={"category": "project_specs", "version": "1.0.0"}
    )
    
    # Ghi nhật ký vào chat history
    await context_manager.log_chat(
        role="system",
        content="Hệ thống đã tự động ghi nhớ toàn bộ thông số kỹ thuật của dự án LanChi.",
        project_id="lanchi_internal"
    )
    
    print("Success! Project specs saved to long-term memory.")

if __name__ == "__main__":
    asyncio.run(save_lanchi_specs())
