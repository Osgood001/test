# Life Coach ｜ 生活教练

一个从零开始的静态网页，展示“生活教练”日常工具版本的概念设计，包含状态感知、主动干预、思维工具、周期性总结与扩展性示例。现在增加了 Python 后端（FastAPI）与 SDK，支持通过 API 生成引导与反思提示。

## 本地查看

1. 安装依赖：`pip install -r requirements.txt`
2. 启动后端（默认 8000 端口）：`uvicorn backend.app:app --reload --port 8000`
3. 在仓库根目录运行一个本地静态服务器以打开前端（任选其一）：
   - `python -m http.server 3000`
   - 或使用任意静态服务器工具。
4. 浏览器访问 http://localhost:3000 体验页面。前端会调用后端 API 生成提示；如果后端未运行，会自动退回前端离线规则。

## Python SDK 使用示例

```python
from backend.sdk import LifeCoachClient

client = LifeCoachClient()
intervention = client.generate_intervention(
    state="被动", mood="分心", blocker="缺少优先级", tone="坚定"
)
reflection = client.generate_reflection(
    day_quality="一般",
    highlight="完成晨间写作 500 字",
    block="刷手机过久",
    experiment="睡前放手机在客厅",
)
print(intervention["combined"])
print(reflection["combined"])
```

## 功能概览

- 状态感知：支持主动/被动/Coach 侧的信号清单。
- 高质量引导：根据状态与情绪生成即时提示和 life hack 建议。
- 思维工具：收录自用与通用的思维框架快速参考。
- 周期性总结：提供日/周/月的量化反思与目标记录占位。
- 扩展性：展示与闹钟、快捷指令、表格量化等常见工具的组合思路。
