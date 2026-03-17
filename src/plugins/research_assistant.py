import logging
from src.context import context_manager

logger = logging.getLogger("lanchi.skills.research")

async def execute(topic: str = None, depth: str = "basic", **kwargs):
    """
    Logic for the research_assistant skill.
    This skill demonstrates the transition from 'Action' (AgentSkill) to 'Memory' (OneContext).
    """
    if not topic:
        return "Missing topic for research."

    logger.info(f"Starting research on: {topic} (depth: {depth})")

    # 1. Simulate finding information (Agent action)
    findings = [
        f"Topic: {topic}",
        f"Summary: Information discovered by LanChi Agent dynamic skills for {topic}.",
        f"Timestamp: 2026-03-15",
        "Source: Simulated Web Research"
    ]
    
    if depth == "deep":
        findings.append("Detailed analysis: This topic has significant long-term relevance for the current project context.")

    content_to_save = "\n".join(findings)

    # 2. Bridge to OneContext: Automatically save findings to Vector DB
    # Now the agent 'knows' this information for next time
    await context_manager.add_context(
        text=content_to_save,
        metadata={"source": "research_assistant", "topic": topic}
    )

    return f"Research completed for '{topic}'. The results have been automatically indexed into OneContext memory for future reference."
