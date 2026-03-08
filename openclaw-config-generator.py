#!/usr/bin/env python3
"""
OpenClaw 配置生成器
一键生成 OpenClaw 配置文件

作者: 贾维斯 (Jarvis)
GitHub: https://github.com/illbnm/openclaw-cost-monitor
捐赠: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)
"""

import json
from pathlib import Path

def generate_openclaw_config(
    name="My Assistant",
    model="claude-3-5-sonnet-20241022",
    skills=None,
    tools=None,
    mcp_servers=None
):
    """生成 OpenClaw 配置"""
    
    config = {
        "name": name,
        "model": model,
        "system": f"You are {name}, a helpful AI assistant.",
        "skills": skills or [],
        "tools": tools or ["read", "write", "edit", "exec", "web_fetch"],
        "mcpServers": mcp_servers or {}
    }
    
    return config

def generate_models_config(models=None):
    """生成 models.json 配置"""
    
    default_models = models or {
        "claude-3-5-sonnet": {
            "api_key": "YOUR_API_KEY",
            "base_url": "https://api.anthropic.com",
            "model": "claude-3-5-sonnet-20241022"
        },
        "gpt-4o": {
            "api_key": "YOUR_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o"
        },
        "gpt-4o-mini": {
            "api_key": "YOUR_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini"
        }
    }
    
    return {"models": default_models}

def main():
    print("🦞 OpenClaw 配置生成器")
    print("=" * 50)
    print()
    
    # 生成基础配置
    config = generate_openclaw_config(
        name="贾维斯 (Jarvis)",
        model="claude-3-5-sonnet-20241022",
        skills=["capability-evolver", "self-improving-agent"],
        tools=["read", "write", "edit", "exec", "web_fetch", "browser", "memory_search", "memory_get"]
    )
    
    print("📄 OpenClaw 配置示例:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print()
    
    # 生成 models.json
    models = generate_models_config()
    print("📄 Models 配置示例:")
    print(json.dumps(models, indent=2, ensure_ascii=False))
    print()
    
    # 保存示例
    output_dir = Path("/tmp/openclaw-config")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    with open(output_dir / "models.json", "w") as f:
        json.dump(models, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置文件已保存到: {output_dir}")
    print()
    print("☕ 捐杯咖啡: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm")

if __name__ == "__main__":
    main()
