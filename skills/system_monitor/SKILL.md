---
name: system_monitor
description: "Monitors system resources including CPU, RAM, Disk, and Network status."
parameters:
  detail_level:
    type: string
    description: "Level of detail: 'basic' or 'full'."
    default: "basic"
---

# System Monitor Skill

This skill allows LanChi to provide real-time hardware telemetry.

### Capabilities:
- **CPU**: Load percentage and core count (logical/physical).
- **Memory**: Total, used, and available percentage.
- **Disk**: Usage of the primary partition.
- **Bot Context**: If running within the LanChi ecosystem.
