---
name: context_summarizer
description: "Tự động tóm tắt các đoạn hội thoại hoặc tài liệu dài thành các sự thật (facts) ngắn gọn để tối ưu hóa bộ nhớ OneContext."
parameters:
  text:
    type: string
    description: "Văn bản hoặc đoạn hội thoại cần tóm tắt."
  mode:
    type: string
    description: "Chế độ tóm tắt: 'facts' (danh sách các sự kiện), 'abstract' (đoạn văn tóm tắt), 'keywords' (từ khóa chính)."
    default: "facts"
  project_id:
    type: string
    description: "ID dự án để định danh ngữ cảnh."
    default: "default"
---

# Context Summarizer Skill

Kỹ năng nén ngữ cảnh giúp LanChi:
- Giảm nhiễu thông tin trong OneContext.
- Tiết kiệm token khi AI truy xuất bộ nhớ dài hạn.
- Trích xuất các thực thể và sự thật quan trọng từ các cuộc họp hoặc tài liệu nghiên cứu dài.

Cách hoạt động:
1. Nhận văn bản thô.
2. Phân tích các ý chính dựa trên chế độ đã chọn.
3. Trả về nội dung đã nén sẵn sàng để nạp vào `memorize_info`.
