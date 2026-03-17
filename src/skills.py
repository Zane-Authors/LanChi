import os
import yaml
import logging
import importlib.util
from typing import Dict, Any, List

logger = logging.getLogger("lanchi.skills")

class SkillManager:
    """
    Manages AgentSkills capabilities according to the agentskills.io pattern.
    Skills are loaded from the 'skills/' folder.
    """
    def __init__(self, skills_dir: str = "skills", plugins_dir: str = "src/plugins"):
        # Normalize paths relative to project root
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.skills_dir = os.path.join(self.root_dir, skills_dir)
        self.plugins_dir = os.path.join(self.root_dir, plugins_dir)
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
            
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)

        # 1. Quét thư mục skills để tìm định nghĩa (Interface)
        for skill_name in os.listdir(self.skills_dir):
            skill_folder = os.path.join(self.skills_dir, skill_name)
            if not os.path.isdir(skill_folder):
                continue

            metadata = None
            # Ưu tiên config.yaml, sau đó đến SKILL.md frontmatter
            config_path = os.path.join(skill_folder, "config.yaml")
            skill_md_path = os.path.join(skill_folder, "SKILL.md")

            try:
                if os.path.exists(config_path):
                    with open(config_path, "r", encoding="utf-8") as f:
                        metadata = yaml.safe_load(f)
                elif os.path.exists(skill_md_path):
                    with open(skill_md_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                metadata = yaml.safe_load(parts[1])

                if not metadata:
                    continue

                # 2. Tìm logic tương ứng trong src/plugins/ (Implementation)
                # Tách biệt code khỏi folder skills mà IDE nhìn thấy
                logic_path = os.path.join(self.plugins_dir, f"{skill_name}.py")
                handler = None
                if os.path.exists(logic_path):
                    handler = self._load_handler_from_file(skill_name, logic_path)

                self.skills[skill_name] = {
                    "metadata": metadata,
                    "handler": handler,
                    "interface_path": skill_folder,
                    "logic_path": logic_path if os.path.exists(logic_path) else None
                }
                logger.info(f"Loaded skill: {skill_name} (Logic: {'Found' if handler else 'Not Found'})")
            except Exception as e:
                logger.error(f"Failed to load skill {skill_name}: {e}")

    def _load_handler_from_file(self, skill_name: str, file_path: str):
        try:
            # Dùng absolute path để tránh lỗi import trên Windows
            abs_path = os.path.abspath(file_path)
            spec = importlib.util.spec_from_file_location(f"lanchi.plugins.{skill_name}", abs_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "execute"):
                return module.execute
        except Exception as e:
            logger.error(f"Error loading logic for skill {skill_name} from {file_path}: {e}")
        return None

    async def execute_skill(self, name: str, **kwargs) -> Any:
        if name not in self.skills:
            return f"Skill '{name}' not found."
        
        skill = self.skills[name]
        handler = skill.get("handler")
        
        if handler:
            try:
                # If it's a coroutine, await it
                import asyncio
                if asyncio.iscoroutinefunction(handler):
                    return await handler(**kwargs)
                return handler(**kwargs)
            except Exception as e:
                return f"Error executing skill '{name}': {str(e)}"
        
        return f"Skill '{name}' loaded but has no 'execute' function in logic.py."

    def list_loaded_skills(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": name,
                "description": info["metadata"].get("description", ""),
                "parameters": info["metadata"].get("parameters", {})
            }
            for name, info in self.skills.items()
        ]

    def reload_skills(self):
        """Clears and reloads all skills from the directory."""
        self.skills = {}
        self.load_skills()
        logger.info("Skills reloaded manually.")

# Simple instantiation
skill_manager = SkillManager()
