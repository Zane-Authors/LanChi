import datetime
try:
    import pytz
except ImportError:
    pytz = None

async def execute(action: str, data: str, from_tz: str = "Asia/Ho_Chi_Minh", to_tz: str = "UTC", **kwargs):
    """
    Logic thực thi cho skill_time_scheduler.
    """
    if action == "convert_tz":
        if not pytz:
            return "Lỗi: Thư viện 'pytz' chưa được cài đặt trên server. Hãy yêu cầu admin cài đặt để sử dụng tính năng chuyển múi giờ."
        
        try:
            # Giả định format 'YYYY-MM-DD HH:MM'
            dt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M")
            local_tz = pytz.timezone(from_tz)
            target_tz = pytz.timezone(to_tz)
            
            local_dt = local_tz.localize(dt)
            target_dt = local_dt.astimezone(target_tz)
            
            return f"Kết quả: {data} tại {from_tz} tương đương với {target_dt.strftime('%Y-%m-%d %H:%M:%S')} tại {to_tz}."
        except Exception as e:
            return f"Lỗi xử lý múi giờ: {str(e)}"

    elif action == "calculate_duration":
        try:
            # Giả định data là 'start_time, end_time' format 'YYYY-MM-DD HH:MM'
            parts = data.split(",")
            start = datetime.datetime.strptime(parts[0].strip(), "%Y-%m-%d %H:%M")
            end = datetime.datetime.strptime(parts[1].strip(), "%Y-%m-%d %H:%M")
            duration = end - start
            return f"Khoảng thời gian giữa {parts[0]} và {parts[1]} là: {duration}."
        except Exception as e:
            return f"Lỗi tính toán khoảng thời gian: {str(e)}. (Gợi ý format: '2026-03-10 09:00, 2026-03-11 10:30')"

    elif action == "suggest_schedule":
        # Một logic đơn giản để phác thảo lịch trình từ văn bản
        schedule_template = f"""
📅 PHÁC THẢO LỊCH TRÌNH CÔNG VIỆC
----------------------------------
Nội dung gốc: {data[:100]}...

Đề xuất thực hiện:
1. Giai đoạn chuẩn bị: {datetime.date.today() + datetime.timedelta(days=1)}
2. Giai đoạn triển khai: {datetime.date.today() + datetime.timedelta(days=3)}
3. Đánh giá kết quả: {datetime.date.today() + datetime.timedelta(days=7)}

Tiến độ đề xuất: Trung bình 2 giờ/ngày.
        """
        return schedule_template

    else:
        return f"Hành động '{action}' không được hỗ trợ bởi skill_time_scheduler."
