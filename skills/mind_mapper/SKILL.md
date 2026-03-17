---
name: mind_mapper
description: "Tạo sơ đồ mạng lưới quan hệ (Relationship Graph) từ văn bản và trả về định dạng HTML/SVG trực quan."
parameters:
  data:
    type: string
    description: "Dữ liệu sơ đồ dạng text (ví dụ: 'LanChi -> Bridge; Bridge -> Stdio')."
  title:
    type: string
    description: "Tiêu đề của sơ đồ."
    default: "LanChi Relationship Map"
---

# Relationship Mapper Skill (Powered by Pyvis)

Kỹ năng này giúp trực quan hóa cấu trúc kiến thức mà không cần cài đặt phần mềm bên ngoài (như Graphviz).

Tính năng:
- Sử dụng Pyvis và NetworkX để xây dựng cấu trúc quan hệ.
- Tự động tạo bản đồ tương quan từ các cặp quan hệ 'A -> B'.
- Trả về mã HTML/SVG có thể hiển thị trực tiếp.

Cách sử dụng:
- Liệt kê các quan hệ ngăn cách bằng dấu chấm phẩy, ví dụ: 'Agent -> Skills; Skills -> Calculator'.
