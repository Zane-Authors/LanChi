import re

async def execute(text: str, mode: str = "facts", project_id: str = "default", **kwargs):
    """
    Logic nén ngữ cảnh và trích xuất sự thật (Facts).
    """
    if not text or len(text.strip()) < 10:
        return "Văn bản quá ngắn để tóm tắt."

    # Xử lý làm sạch văn bản cơ bản
    clean_text = text.replace("\n", " ").strip()
    
    if mode == "keywords":
        # Trích xuất từ khóa đơn giản (các từ viết hoa hoặc từ dài)
        words = re.findall(r'\b\w{5,}\b', clean_text)
        keywords = list(set(words))[:15]
        return f"Từ khóa chính: {', '.join(keywords)}"

    elif mode == "abstract":
        # Tóm tắt đoạn văn (Lấy ~30% văn bản ở mức cơ bản)
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        if len(sentences) <= 3:
            return clean_text
        
        summary = " ".join(sentences[:2] + sentences[-1:])
        return f"[Tóm tắt] {summary}"

    else:  # default mode: facts
        # Trích xuất các ý chính (Bullets)
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        facts = []
        for s in sentences:
            s = s.strip()
            # Heuristic: Những câu có số, ngày tháng, hoặc thực thể thường là facts
            if len(s) > 20 and (re.search(r'\d', s) or len(re.findall(r'[A-Z]', s)) > 2):
                facts.append(f"- {s}")
        
        if not facts:
            # Nếu không tìm thấy facts đặc biệt, lấy các câu đầu tiên làm Key Facts
            facts = [f"- {s}" for s in sentences[:3]]

        header = f"📋 HỒ SƠ SỰ THẬT (PROJECT: {project_id})\n"
        return header + "\n".join(facts)
