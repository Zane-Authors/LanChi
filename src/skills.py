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
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
            return

        for skill_name in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_name)
            if not os.path.isdir(skill_path):
                continue

            skill_md_path = os.path.join(skill_path, "SKILL.md")
            if not os.path.exists(skill_md_path):
                continue

            try:
                with open(skill_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.startswith("---"):
                        _, frontmatter, _ = content.split("---", 2)
                        metadata = yaml.safe_load(frontmatter)
                        
                        # Look for logic.py in the skill folder
                        logic_path = os.path.join(skill_path, "logic.py")
                        handler = None
                        if os.path.exists(logic_path):
                            handler = self._load_handler_from_file(skill_name, logic_path)

                        self.skills[skill_name] = {
                            "metadata": metadata,
                            "path": skill_path,
                            "handler": handler
                        }
                        logger.info(f"Loaded skill: {skill_name}")
            except Exception as e:
                logger.error(f"Failed to load skill {skill_name}: {e}")

    def _load_handler_from_file(self, skill_name: str, file_path: str):
        try:
            spec = importlib.util.spec_from_file_location(f"skill_{skill_name}", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "execute"):
                return module.execute
        except Exception as e:
            logger.error(f"Error loading logic for skill {skill_name}: {e}")
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
