import os
import json
try:
    import networkx as nx
    from pyvis.network import Network
except ImportError:
    nx = None

async def execute(data: str, title: str = "LanChi Relationship Map", **kwargs):
    """
    Tạo sơ đồ quan hệ sử dụng Pyvis (Thuần Python, không cần Graphviz bin).
    """
    if nx is None:
        return "Lỗi: Thư viện 'pyvis' hoặc 'networkx' chưa được cài đặt."

    try:
        # 1. Khởi tạo Graph
        G = nx.MultiDiGraph()
        
        # 2. Parse dữ liệu 'A -> B'
        lines = data.split(';')
        for line in lines:
            line = line.strip()
            if '->' in line:
                parts = line.split('->')
                if len(parts) >= 2:
                    src = parts[0].strip()
                    dst = parts[1].strip()
                    G.add_edge(src, dst)
            elif line:
                G.add_node(line)

        if len(G.nodes) == 0:
            return "Dữ liệu sơ đồ trống hoặc không đúng định dạng 'A -> B'."

        # 3. Sử dụng Pyvis để render ra HTML string
        net = Network(height="500px", width="100%", heading=title, directed=True, bgcolor="#222222", font_color="white")
        net.from_nx(G)
        
        # Cấu hình vật lý
        net.toggle_physics(True)
        
        # Lấy HTML content trực tiếp từ Pyvis (tránh lỗi file encoding trên Windows)
        html_content = net.generate_html()
        
        # Trả về kết quả
        return f"--- {title} ---\n\nSơ đồ đã được tạo thành công (Pure Python). Bạn có thể lưu mã này vào file .html để xem:\n\n{html_content[:500]}... [Dữ liệu HTML (UTF-8) đã sẵn sàng]"

    except Exception as e:
        return f"Lỗi khi xử lý sơ đồ: {str(e)}"
