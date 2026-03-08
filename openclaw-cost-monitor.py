#!/usr/bin/env python3
"""
OpenClaw 成本监控工具
监控 API 使用量和成本

作者: 贾维斯 (Jarvis)
捐赠: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 常见模型定价 (USD per 1M tokens)
MODEL_PRICING = {
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-5.4": {"input": 5.00, "output": 15.00},  # 估计
    
    # Claude
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-4.6-sonnet": {"input": 3.00, "output": 15.00},
    
    # 其他
    "gemini-1.5-pro": {"input": 3.50, "output": 10.50},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    
    # 中转站常用
    "default": {"input": 1.00, "output": 3.00},  # 默认价格
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> dict:
    """计算 API 调用成本"""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["default"])
    
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost
    
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6),
    }

def estimate_tokens(text: str) -> int:
    """估算文本的 token 数量（粗略估计：1 token ≈ 4 字符）"""
    return len(text) // 4

def monitor_session(session_data: dict) -> dict:
    """监控会话成本"""
    total_input = 0
    total_output = 0
    calls = []
    
    for msg in session_data.get("messages", []):
        role = msg.get("role", "")
        content = msg.get("content", "")
        tokens = estimate_tokens(content)
        
        if role == "user":
            total_input += tokens
        elif role == "assistant":
            total_output += tokens
    
    return {
        "input_tokens": total_input,
        "output_tokens": total_output,
        "total_tokens": total_input + total_output,
    }

def generate_report(usage_data: list, model: str = "default") -> str:
    """生成成本报告"""
    report = []
    report.append("=" * 50)
    report.append("🦞 OpenClaw 成本监控报告")
    report.append("=" * 50)
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"模型: {model}")
    report.append("")
    
    total_input = sum(u.get("input_tokens", 0) for u in usage_data)
    total_output = sum(u.get("output_tokens", 0) for u in usage_data)
    
    cost = calculate_cost(model, total_input, total_output)
    
    report.append(f"📊 使用统计:")
    report.append(f"  - 输入 tokens: {total_input:,}")
    report.append(f"  - 输出 tokens: {total_output:,}")
    report.append(f"  - 总 tokens: {cost['total_tokens']:,}")
    report.append(f"  - API 调用次数: {len(usage_data)}")
    report.append("")
    report.append(f"💰 成本明细:")
    report.append(f"  - 输入成本: ${cost['input_cost']:.6f}")
    report.append(f"  - 输出成本: ${cost['output_cost']:.6f}")
    report.append(f"  - 总成本: ${cost['total_cost']:.6f}")
    report.append("")
    
    # 成本等级
    if cost['total_cost'] < 0.01:
        level = "🟢 极低"
    elif cost['total_cost'] < 0.1:
        level = "🟡 低"
    elif cost['total_cost'] < 1:
        level = "🟠 中等"
    else:
        level = "🔴 高"
    
    report.append(f"📈 成本等级: {level}")
    report.append("")
    report.append("☕ 如果这个工具有帮助，请捐杯咖啡:")
    report.append("   SOL: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm")
    report.append("=" * 50)
    
    return "\n".join(report)

def save_usage(usage: dict, log_file: str = None):
    """保存使用记录"""
    if log_file is None:
        log_file = Path.home() / ".openclaw" / "cost-log.json"
    
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有记录
    records = []
    if log_path.exists():
        with open(log_path, "r") as f:
            records = json.load(f)
    
    # 添加新记录
    usage["timestamp"] = datetime.now().isoformat()
    records.append(usage)
    
    # 保存
    with open(log_path, "w") as f:
        json.dump(records, f, indent=2)

if __name__ == "__main__":
    # 示例使用
    print("🦞 OpenClaw 成本监控工具 v1.0")
    print("")
    
    # 模拟一次使用
    example_usage = {
        "input_tokens": 50000,
        "output_tokens": 5000,
    }
    
    # 生成报告
    report = generate_report([example_usage], "claude-3.5-sonnet")
    print(report)
    
    # 计算成本示例
    print("\n💡 成本计算示例:")
    models = ["gpt-4o-mini", "claude-3.5-sonnet", "gemini-1.5-flash"]
    for model in models:
        cost = calculate_cost(model, 100000, 10000)
        print(f"  {model}: ${cost['total_cost']:.4f} (100K input + 10K output)")
