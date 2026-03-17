import math
import operator

# Thư viện các toán tử và hàm số an toàn
SAFE_NAMES = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'pow': pow,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'pi': math.pi,
    'e': math.e,
}

def execute(expression: str = None, **kwargs):
    """
    Logic nâng cao cho skill tính toán, sử dụng eval an toàn.
    """
    if not expression:
        return "Vui lòng cung cấp biểu thức toán học."
    
    # Tiền xử lý: thay thế ^ bằng ** cho lũy thừa
    expr = expression.replace('^', '**')
    
    try:
        # Sử dụng eval với danh sách whitelist các hàm và không có builtins độc hại
        # Điều này an toàn hơn nhiều so với eval mặc định
        result = eval(expr, {"__builtins__": None}, SAFE_NAMES)
        
        # Format kết quả
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 10)
            
        return f"Kết quả: {result}"
    except SyntaxError:
        return "Lỗi cú pháp trong biểu thức."
    except NameError as e:
        return f"Lỗi: Hàm hoặc biến không được hỗ trợ ({str(e)})"
    except ZeroDivisionError:
        return "Lỗi: Không thể chia cho 0."
    except Exception as e:
        return f"Lỗi khi tính toán: {str(e)}"
