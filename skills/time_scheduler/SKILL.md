---
name: time_scheduler
description: "Quản lý thời gian, tính toán khoảng cách giữa các sự kiện và lập lịch công việc dựa trên nghiên cứu."
parameters:
  action:
    type: string
    description: "Hành động cần thực hiện: 'convert_tz' (chuyển múi giờ), 'calculate_duration' (tính khoảng thời gian), 'suggest_schedule' (gợi ý lịch trình từ văn bản)."
  data:
    type: string
    description: "Dữ liệu đầu vào (Ví dụ: '2026-03-20 09:00', hoặc một đoạn văn bản kế hoạch)."
  from_tz:
    type: string
    description: "Múi giờ gốc (Ví dụ: 'UTC', 'Asia/Ho_Chi_Minh'). Mặc định là 'Asia/Ho_Chi_Minh'."
    default: "Asia/Ho_Chi_Minh"
  to_tz:
    type: string
    description: "Múi giờ đích."
    default: "UTC"
---

# Time Scheduler Skill

Kỹ năng quản lý thời gian mạnh mẽ cho LanChi giúp:
- Chuyển đổi múi giờ linh hoạt (hỗ trợ toàn bộ cơ sở dữ liệu pytz).
- Tính toán khoảng thời gian (duration) giữa các cột mốc.
- Đề xuất lịch trình công việc từ các kết quả nghiên cứu.

Cách sử dụng:
- **convert_tz**: Cần `data` (datetime string) và `from_tz`, `to_tz`.
- **calculate_duration**: Cần `data` (là 2 chuỗi thời gian cách nhau bởi dấu phẩy).
- **suggest_schedule**: Cần `data` (văn bản mô tả kế hoạch).
