import psutil
import os
import platform
import datetime

async def execute(detail_level="basic", **kwargs):
    """
    Monitors system resources.
    """
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    if detail_level == "full":
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"
        
        return {
            "summary": f"System Status: CPU {cpu_percent}%, RAM {memory.percent}% used.",
            "os": platform.system() + " " + platform.release(),
            "cpu": {
                "usage_percent": cpu_percent,
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(logical=True),
                "frequency_mhz": cpu_freq
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_percent": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2)
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_percent": disk.percent,
                "free_gb": round(disk.free / (1024**3), 2)
            },
            "boot_time": boot_time
        }
    
    return (
        f"🖥️ System Monitor (Basic):\n"
        f"- CPU Usage: {cpu_percent}%\n"
        f"- RAM: {memory.percent}% ({round(memory.available / (1024**3), 2)}GB Free)\n"
        f"- Disk: {disk.percent}% used on primary drive."
    )
