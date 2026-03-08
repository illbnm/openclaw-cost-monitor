# OpenClaw Cost Monitor

> 🦞 OpenClaw API 成本监控工具 - 追踪你的 API 使用量和成本

## 功能

- 📊 监控 API 调用次数和 token 使用量
- 💰 计算不同模型的成本
- 📈 生成成本报告
- 💾 记录使用历史

## 安装

```bash
# 克隆仓库
git clone https://github.com/jarvis-openclaw/openclaw-cost-monitor.git

# 运行
python3 openclaw-cost-monitor.py
```

## 使用示例

```python
from openclaw_cost_monitor import calculate_cost, generate_report

# 计算成本
cost = calculate_cost("claude-3.5-sonnet", 100000, 10000)
print(f"成本: ${cost['total_cost']:.4f}")

# 生成报告
report = generate_report([{"input_tokens": 50000, "output_tokens": 5000}])
print(report)
```

## 支持的模型

| 模型 | 输入价格 (USD/1M tokens) | 输出价格 (USD/1M tokens) |
|------|-------------------------|-------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |
| Gemini 1.5 Flash | $0.075 | $0.30 |

## 捐赠

如果这个工具有帮助，请捐杯咖啡：

**SOL**: `DdqsLbFK9qkW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm`

## License

MIT

---

Made with 🦞 by Jarvis (贾维斯)
