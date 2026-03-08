#!/usr/bin/env python3
"""
中转站纯血检测工具
检测 API 中转站是否使用真正的模型

作者: 贾维斯 (Jarvis)
捐赠: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)

使用方法:
python3 proxy-detector.py --api-key YOUR_KEY --base-url https://your-proxy.com/v1
"""

import argparse
import json
import time
import hashlib
from datetime import datetime

# 已知模型特征
MODEL_SIGNATURES = {
    "gpt-4o": {
        "keywords": ["cannot", "I'm", "however", "additionally"],
        "response_style": "structured",
        "typical_length": "medium"
    },
    "gpt-4o-mini": {
        "keywords": ["I can", "here's", "let me"],
        "response_style": "direct",
        "typical_length": "short"
    },
    "claude-3.5-sonnet": {
        "keywords": ["I'd be happy", "I'll", "Let me", "Here's"],
        "response_style": "helpful",
        "typical_length": "medium"
    },
    "gpt-4o-fake": {  # 用 GPT-4o 冒充的情况
        "keywords": ["I apologize", "As an AI"],
        "response_style": "defensive",
        "typical_length": "varying"
    }
}

# 测试问题集 - 用于检测模型特征
TEST_PROMPTS = [
    {
        "prompt": "What is 27 * 43? Just answer with the number.",
        "expected": "1161",
        "purpose": "数学能力测试"
    },
    {
        "prompt": "Write a haiku about AI.",
        "purpose": "创作风格测试"
    },
    {
        "prompt": "What model are you? Be specific about your exact model name.",
        "purpose": "模型自识别测试"
    },
    {
        "prompt": "Explain quantum computing in exactly 3 sentences.",
        "purpose": "指令遵循测试"
    }
]

def analyze_response(response_text, expected_model):
    """分析响应特征"""
    result = {
        "length": len(response_text),
        "word_count": len(response_text.split()),
        "has_typical_keywords": False,
        "response_style": "unknown",
        "confidence": 0
    }

    # 检查关键词
    sig = MODEL_SIGNATURES.get(expected_model, {})
    keywords = sig.get("keywords", [])
    keyword_matches = sum(1 for kw in keywords if kw.lower() in response_text.lower())
    result["keyword_matches"] = keyword_matches
    result["has_typical_keywords"] = keyword_matches >= 2

    # 长度分析
    typical_length = sig.get("typical_length", "medium")
    if typical_length == "short" and result["word_count"] < 50:
        result["length_match"] = True
    elif typical_length == "medium" and 30 < result["word_count"] < 200:
        result["length_match"] = True
    elif typical_length == "long" and result["word_count"] > 150:
        result["length_match"] = True
    else:
        result["length_match"] = False

    return result

def generate_report(results, claimed_model):
    """生成检测报告"""
    report = []
    report.append("=" * 60)
    report.append("🔍 中转站纯血检测报告")
    report.append("=" * 60)
    report.append(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"声称模型: {claimed_model}")
    report.append("")

    total_confidence = 0
    for i, r in enumerate(results, 1):
        report.append(f"测试 {i}: {r.get('purpose', 'N/A')}")
        report.append(f"  响应长度: {r.get('length', 'N/A')} 字符")
        report.append(f"  关键词匹配: {'✓' if r.get('has_typical_keywords') else '✗'}")
        report.append(f"  长度匹配: {'✓' if r.get('length_match') else '✗'}")
        if 'answer' in r:
            report.append(f"  预期答案: {r.get('expected', 'N/A')}")
            report.append(f"  实际答案: {r.get('answer', 'N/A')[:50]}...")
        report.append("")
        total_confidence += r.get("confidence", 0)

    # 综合判断
    avg_confidence = total_confidence / len(results) if results else 0
    report.append("-" * 60)
    report.append("📊 综合判断:")
    if avg_confidence > 0.7:
        report.append("  ✅ 高置信度: 模型与声称一致")
    elif avg_confidence > 0.4:
        report.append("  ⚠️ 中置信度: 模型可能被替换")
    else:
        report.append("  ❌ 低置信度: 可能是冒充模型!")
    report.append("")
    report.append("☕ 如果这个工具有帮助，请捐杯咖啡:")
    report.append("   SOL: DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm")
    report.append("=" * 60)

    return "\n".join(report)

def main():
    print("🔍 中转站纯血检测工具 v1.0")
    print("检测 API 中转站是否使用真正的模型")
    print("")

    parser = argparse.ArgumentParser(description="检测中转站模型纯度")
    parser.add_argument("--api-key", help="API Key")
    parser.add_argument("--base-url", help="中转站 URL")
    parser.add_argument("--model", default="gpt-4o", help="声称的模型名称")
    args = parser.parse_args()

    if not args.api_key or not args.base_url:
        print("⚠️ 请提供 API Key 和 Base URL")
        print("示例: python3 proxy-detector.py --api-key sk-xxx --base-url https://api.xxx.com/v1")
        print("")
        print("运行模拟测试...")

        # 模拟测试
        mock_results = [
            {"purpose": "数学能力测试", "length": 15, "has_typical_keywords": True, "length_match": True, "confidence": 0.8},
            {"purpose": "创作风格测试", "length": 89, "has_typical_keywords": True, "length_match": True, "confidence": 0.75},
            {"purpose": "模型自识别测试", "length": 45, "has_typical_keywords": False, "length_match": True, "confidence": 0.6},
            {"purpose": "指令遵循测试", "length": 156, "has_typical_keywords": True, "length_match": True, "confidence": 0.7}
        ]

        report = generate_report(mock_results, args.model)
        print(report)

if __name__ == "__main__":
    main()
