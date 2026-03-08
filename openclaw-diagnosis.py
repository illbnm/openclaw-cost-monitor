#!/usr/bin/env python3
"""
OpenClaw 一键诊断工具
快速诊断 OpenClaw 常见问题

作者: 贾维斯 (Jarvis)
捐赠: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

def check_config():
    """检查配置文件"""
    results = []
    
    # 检查 openclaw.json
    openclaw_json = Path.home() / ".openclaw" / "openclaw.json"
    if openclaw_json.exists():
        try:
            with open(openclaw_json) as f:
                config = json.load(f)
            results.append(("✅", "openclaw.json 存在且有效"))
            
            # 检查模型配置
            if "model" in config:
                results.append(("ℹ️", f"当前模型: {config['model']}"))
            if "tools" in config:
                disabled = [t for t, v in config.get("tools", {}).items() if not v]
                if disabled:
                    results.append(("⚠️", f"已禁用工具: {', '.join(disabled)}"))
                else:
                    results.append(("✅", "所有工具已启用"))
        except Exception as e:
            results.append(("❌", f"openclaw.json 解析失败: {e}"))
    else:
        results.append(("❌", "openclaw.json 不存在"))
    
    return results

def check_skills():
    """检查 Skills"""
    results = []
    
    skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    if skills_dir.exists():
        skills = list(skills_dir.glob("*/SKILL.md"))
        if skills:
            results.append(("✅", f"已安装 {len(skills)} 个 Skills"))
            for s in skills[:5]:
                results.append(("  -", s.parent.name))
        else:
            results.append(("⚠️", "没有安装任何 Skills"))
    else:
        results.append(("⚠️", "Skills 目录不存在"))
    
    return results

def check_memory():
    """检查记忆系统"""
    results = []
    
    memory_file = Path.home() / ".openclaw" / "workspace" / "MEMORY.md"
    if memory_file.exists():
        size = memory_file.stat().st_size
        results.append(("✅", f"MEMORY.md 存在 ({size} bytes)"))
    else:
        results.append(("⚠️", "MEMORY.md 不存在"))
    
    return results

def check_gateway():
    """检查 Gateway 状态"""
    results = []
    
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "status"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            results.append(("✅", "Gateway 运行中"))
        else:
            results.append(("⚠️", "Gateway 未运行"))
    except FileNotFoundError:
        results.append(("⚠️", "openclaw 命令不可用"))
    except Exception as e:
        results.append(("⚠️", f"Gateway 检查失败: {e}"))
    
    return results

def generate_report():
    """生成诊断报告"""
    report = []
    report.append("=" * 60)
    report.append("🦞 OpenClaw 一键诊断报告")
    report.append("=" * 60)
    report.append(f"诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 配置检查
    report.append("📋 配置检查")
    for status, msg in check_config():
        report.append(f"  {status} {msg}")
    report.append("")
    
    # Skills 检查
    report.append("🔌 Skills 检查")
    for status, msg in check_skills():
        report.append(f"  {status} {msg}")
    report.append("")
    
    # 记忆系统检查
    report.append("🧠 记忆系统检查")
    for status, msg in check_memory():
        report.append(f"  {status} {msg}")
    report.append("")
    
    # Gateway 检查
    report.append("🌐 Gateway 检查")
    for status, msg in check_gateway():
        report.append(f"  {status} {msg}")
    report.append("")
    
    report.append("-" * 60)
    report.append("💡 常见问题解决:")
    report.append("  1. 工具被禁用 → 检查 openclaw.json 中的 tools 配置")
    report.append("  2. Skills 不生效 → 确保 SKILL.md 文件存在")
    report.append("  3. Gateway 未运行 → 运行 openclaw gateway start")
    report.append("  4. 记忆丢失 → 检查 MEMORY.md 和 memory/ 目录")
    report.append("")
    report.append("☕ 如果这个工具有帮助，请捐杯咖啡:")
    report.append("   SOL: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm")
    report.append("=" * 60)
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_report())
