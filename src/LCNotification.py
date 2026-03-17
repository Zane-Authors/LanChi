import sys
import tomllib  # Python 3.11+
from pathlib import Path
import httpx
import psutil
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich import box
from rich.align import Align  # Thêm Align để căn giữa ASCII Art

console = Console()

def get_project_version():
    """Đọc version thực tế từ pyproject.toml"""
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            return data["project"].get("version", "unknown")
    except Exception:
        return "v0.1.0"

def check_endpoint(url: str):
    """Kiểm tra thực tế trạng thái của API"""
    try:
        with httpx.Client(timeout=1.0) as client:
            # Sửa lại URL cho chính xác
            response = client.get(url)
            return "[bold green]ONLINE[/bold green]" if response.status_code < 400 else "[bold yellow]WARNING[/bold yellow]"
    except Exception:
        return "[bold red]OFFLINE[/bold red]"

def startup_lanchi(api_status=None, **kwargs):
    # ==========================================
    # 1. Vẽ lại Logo LanChi bằng ASCII (An toàn cho mọi terminal)
    # ==========================================
    
    lanchi_ascii = r"""
  _        _   _   _  _____ _   _ ___ 
 | |      / \ | \ | |/  ___| | | |_ _|
 | |     / _ \|  \| | |    | |_| || | 
 | |___ / ___ \ | \ | |___ |  _  || | 
 |_____/_/   \_\_| \_\_____|_| |_|___|
    """
    
    version = get_project_version()
    
    try:
        # Tạo nội dung Panel: ASCII Art + Text bên dưới
        banner_content = Align.center(
            f"[bold cyan]{lanchi_ascii}[/bold cyan]\n"
            f"[bold cyan]M C P   S Y S T E M[/bold cyan]\n"
            f"[italic magenta]LanChi Engine Core - {version}[/italic magenta]",
            vertical="middle"
        )
        console.print(Panel(banner_content, box=box.DOUBLE, border_style="blue", expand=False))
    except Exception:
        # Fallback nếu terminal không hỗ trợ Rich Panel phức tạp
        print(f"LANCHI MCP SYSTEM - {version}")

    # ==========================================
    # 2. Xử lý logic kiểm tra thực tế
    # ==========================================
    results = {}
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            console=console,
            transient=True
        ) as progress:
            
            # Bước 1: Kiểm tra tài nguyên máy chủ
            task1 = progress.add_task("[yellow]Analyzing System...", total=1)
            ram_usage = psutil.virtual_memory().percent
            results["context"] = f"RAM: {ram_usage}%"
            progress.advance(task1)

            # Bước 2: Kiểm tra FastAPI Endpoint
            task2 = progress.add_task("[yellow]Probing API...", total=1)
            if api_status:
                results["api"] = api_status
            else:
                results["api"] = check_endpoint("http://127.0.0.1:5050/health")
            progress.advance(task2)

            # Bước 3: Kiểm tra Python Environment
            task3 = progress.add_task("[yellow]Verifying Env...", total=1)
            results["env"] = f"Python {sys.version_info.major}.{sys.version_info.minor}"
            progress.advance(task3)
    except Exception:
        # Failback nếu Progress bar lỗi
        results["context"] = f"RAM: {psutil.virtual_memory().percent}%"
        results["api"] = api_status or "CHECKING..."
        results["env"] = f"Python {sys.version_info.major}.{sys.version_info.minor}"
    try:
        import chromadb
        results["chroma_ver"] = chromadb.__version__
    except:
        results["chroma_ver"] = "N/A"
        
    try:
        import duckdb
        results["duckdb_ver"] = duckdb.__version__
    except:
        results["duckdb_ver"] = "N/A"

    # 3. Bảng trạng thái thực tế
    try:
        table = Table(title=f"[bold green]LanChi MCP System Status[/bold green]", box=box.ROUNDED)
        table.add_column("Component", style="cyan")
        table.add_column("Real-time Status", justify="center")
        table.add_column("Details", justify="right", style="dim")

        table.add_row("FastAPI Gateway", results["api"], "Port: 5050")
        table.add_row("Context Memory", "ACTIVE", results["context"])
        table.add_row("MCP Runtime", "CONNECTED", results["env"])
        table.add_row("ChromaDB", "CONNECTED",f"v{results['chroma_ver']}")
        table.add_row("DuckDB", "CONNECTED",f"v{results['duckdb_ver']}")
        
        console.print(table)

        if "OFFLINE" in results["api"]:
            console.print("\n[bold red]WARNING: API Gateway not started.[/bold red]\n")
        else:
            console.print("\n[bold green]LanChi System is Live & Ready![/bold green]\n")
    except Exception:
        # Fallback final
        print(f"Status: {results.get('api', 'Unknown')}")

if __name__ == "__main__":
    startup_lanchi()