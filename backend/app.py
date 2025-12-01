"""Life Coach backend with lightweight rule-based AI endpoints."""
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Life Coach Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


PROMPTS: Dict[str, list[str]] = {
    "主动": [
        "你已经开始行动了，保持节奏，先完成最笨的版本。",
        "把目标写下来，拆成 25 分钟的小块，完成一个就打个✅。",
        "记录当下的阻碍，先解决最影响情绪的 1 件事。",
    ],
    "被动": [
        "嗨，你是不是忘记了什么？现在就用 5 分钟拉回节奏。",
        "我猜你有点卡住了——先做“更弱版本”，行动后再优化。",
        "还记得你之前做到过这个吗？复制那次的步骤再试一次。",
    ],
    "Coach": [
        "等一下，我向你确认：你是否需要一个更小的起点？",
        "也许你该关注一个具体指标：写作 200 字 or 10 分钟走动。",
        "喂，别困在那里，立刻试试这个：关掉干扰，设 15 分钟番茄钟。",
    ],
}


LIFE_HACKS = [
    "使用纸笔列出“下一步”三件事，做完一项划掉。",
    "在日历里插入两个 25 分钟专注块，只做一件事。",
    "用手机计时 10 分钟收尾当前任务，结束即可，不求完美。",
    "把手机放到另一间房，开一个番茄钟，结束后再取回。",
    "在文档顶部加一句“我现在要完成的是…”，持续更新。",
    "用 Lesson Log 记录今天的踩坑，并写出下一次怎么做。",
]


TONE_ADDONS: Dict[str, str] = {
    "温和": "温柔提醒：你做得到的，先迈开小一步。",
    "坚定": "现在就行动，先完成 1 个最小成果，然后反馈给我。",
    "紧急": "立刻执行，给自己 5 分钟倒计时，完成后再评估。",
}


MOOD_HINTS: Dict[str, str] = {
    "低落": "先照顾身体：喝水、拉伸 2 分钟，再做 10 分钟微行动。",
    "焦虑": "把脑中的担忧写下来，挑 1 条能在 15 分钟内验证的假设。",
    "分心": "关掉可见的干扰，开 Do Not Disturb，设定专注计时。",
    "平静": "保持节奏感：给自己排三个短任务，按顺序完成。",
}


BLOCKER_HINTS: Dict[str, str] = {
    "缺少优先级": "先选 1 个北极星指标，今天的行动只服务它。",
    "缺少动力": "回忆最近完成的一个小胜利，复制那套开始方式。",
    "缺少结构": "用 WBS 拆成 3 层，保留可执行的最底层行动。",
    "被干扰": "记录干扰来源，设置 30 分钟后再处理的提醒。",
}


class InterventionRequest(BaseModel):
    state: str = Field(..., description="用户当前状态：主动/被动/Coach")
    mood: str = Field(..., description="情绪/体感")
    blocker: str = Field(..., description="当前阻碍")
    tone: str = Field(..., description="反馈风格")


class InterventionResponse(BaseModel):
    opener: str
    tone: str
    mood_hint: str
    blocker_hint: str
    hack: str
    combined: str


class ReflectionRequest(BaseModel):
    dayQuality: str
    highlight: str
    block: str
    experiment: str


class ReflectionResponse(BaseModel):
    summary: str
    next_step: str
    combined: str


def _pick(items: list[str], seed: str) -> str:
    """Pick a deterministic item based on a seed string for stability."""
    if not items:
        return ""
    index = abs(hash(seed)) % len(items)
    return items[index]


def build_intervention(payload: InterventionRequest) -> InterventionResponse:
    opener = _pick(PROMPTS.get(payload.state, PROMPTS["主动"]), payload.state + payload.mood)
    hack = _pick(LIFE_HACKS, payload.state + payload.blocker)
    mood_hint = MOOD_HINTS.get(payload.mood, "留出 5 分钟呼吸并写下当下的感受。")
    blocker_hint = BLOCKER_HINTS.get(payload.blocker, "把任务拆成 10 分钟可完成的动作。")
    tone_text = TONE_ADDONS.get(payload.tone, TONE_ADDONS["温和"])

    combined = "\n".join(
        [
            f"{opener}",
            tone_text,
            mood_hint,
            blocker_hint,
            f"试试这个 life hack：{hack}",
        ]
    )

    return InterventionResponse(
        opener=opener,
        tone=tone_text,
        mood_hint=mood_hint,
        blocker_hint=blocker_hint,
        hack=hack,
        combined=combined,
    )


def build_reflection(payload: ReflectionRequest) -> ReflectionResponse:
    next_step_rules = {
        "一般": "明天挑 1 个最能改善节奏的动作，多做 10%。",
        "优秀": "继续保持，并在日历中锁定两个深度工作块。",
        "低迷": "先找回身心状态：早点睡、简单运动，再做 1 个小目标。",
    }
    next_step = next_step_rules.get(payload.dayQuality, "写下明天最重要的 1 件事，并预约提醒。")
    summary = (
        f"今天：{payload.highlight}\n"
        f"阻碍：{payload.block}\n"
        f"下一步实验：{payload.experiment}"
    )
    combined = "\n".join([summary, f"明日提示：{next_step}"])

    return ReflectionResponse(summary=summary, next_step=next_step, combined=combined)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/intervention", response_model=InterventionResponse)
def generate_intervention(payload: InterventionRequest) -> InterventionResponse:
    """Rule-based intervention generator used as a mock AI endpoint."""
    return build_intervention(payload)


@app.post("/api/reflection", response_model=ReflectionResponse)
def generate_reflection(payload: ReflectionRequest) -> ReflectionResponse:
    """Rule-based daily reflection summarizer."""
    return build_reflection(payload)
