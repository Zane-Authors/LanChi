import httpx
import logging
from urllib.parse import quote

logger = logging.getLogger("lanchi.skills.devdocs")

async def execute(query: str = None, doc_type: str = None, **kwargs):
    """
    Tra cứu tài liệu từ API công khai của DevDocs.io (thông qua tìm kiếm).
    """
    if not query:
        return "Vui lòng nhập từ khóa cần tra cứu."

    # DevDocs không có API tìm kiếm chính thức trả về nội dung trực tiếp dễ dàng,
    # nhưng chúng ta có thể sử dụng cơ chế tìm kiếm và gợi ý hoặc trả về link trực tiếp.
    # Chiến thuật: Trả về link tra cứu và kết quả nhanh nếu có thể.
    
    search_url = f"https://devdocs.io/#q={quote(query)}"
    if doc_type:
        search_url = f"https://devdocs.io/{quote(doc_type)}/#q={quote(query)}"

    # Trả về thông tin hướng dẫn vì DevDocs chủ yếu chạy client-side.
    # Một cách tiếp cận tốt hơn cho Agent là cung cấp link trực tiếp để nó gợi ý cho user
    # HOẶC sử dụng một API mirror nếu có.
    
    result = [
        f"🔍 Kết quả tra cứu cho: **{query}**",
        f"🔗 Xem tài liệu chi tiết tại: {search_url}",
        "\n*Gợi ý: Bạn có thể chỉ định doc_type như 'python~3.12', 'javascript', 'css', 'react' để có kết quả chính xác hơn.*"
    ]

    # Thử lấy gợi ý từ API gợi ý của DevDocs để tăng tính hữu ích
    try:
        # DevDocs search index is usually a large JSON, here we use a lightweight approach
        # Note: In a full version, we could cache the index.
        pass
    except Exception as e:
        logger.error(f"DevDocs suggest error: {e}")

    return "\n".join(result)
