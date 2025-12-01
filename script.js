const prompts = {
  主动: [
    '你已经开始行动了，保持节奏，先完成最笨的版本。',
    '把目标写下来，拆成 25 分钟的小块，完成一个就打个✅。',
    '记录当下的阻碍，先解决最影响情绪的 1 件事。',
  ],
  被动: [
    '嗨，你是不是忘记了什么？现在就用 5 分钟拉回节奏。',
    '我猜你有点卡住了——先做“更弱版本”，行动后再优化。',
    '还记得你之前做到过这个吗？复制那次的步骤再试一次。',
  ],
  Coach: [
    '等一下，我向你确认：你是否需要一个更小的起点？',
    '也许你该关注一个具体指标：写作 200 字 or 10 分钟走动。',
    '喂，别困在那里，立刻试试这个：关掉干扰，设 15 分钟番茄钟。',
  ],
};

const lifeHacks = [
  '使用纸笔列出“下一步”三件事，做完一项划掉。',
  '在日历里插入两个 25 分钟专注块，只做一件事。',
  '用手机计时 10 分钟收尾当前任务，结束即可，不求完美。',
  '把手机放到另一间房，开一个番茄钟，结束后再取回。',
  '在文档顶部加一句“我现在要完成的是…”，持续更新。',
  '用 Lesson Log 记录今天的踩坑，并写出下一次怎么做。',
];

const toneAddons = {
  温和: '温柔提醒：你做得到的，先迈开小一步。',
  坚定: '现在就行动，先完成 1 个最小成果，然后反馈给我。',
  紧急: '立刻执行，给自己 5 分钟倒计时，完成后再评估。',
};

function randomPick(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function generateIntervention(event) {
  event.preventDefault();
  const form = event.target;
  const state = form.state.value;
  const mood = form.mood.value;
  const blocker = form.blocker.value;
  const tone = form.tone.value;

  const opener = randomPick(prompts[state]);
  const hack = randomPick(lifeHacks);
  const toneText = toneAddons[tone];

  const moodNudge = {
    低落: '先照顾身体：喝水、拉伸 2 分钟，再做 10 分钟微行动。',
    焦虑: '把脑中的担忧写下来，挑 1 条能在 15 分钟内验证的假设。',
    分心: '关掉可见的干扰，开 Do Not Disturb，设定专注计时。',
    平静: '保持节奏感：给自己排三个短任务，按顺序完成。',
  }[mood];

  const blockerHint = {
    缺少优先级: '先选 1 个北极星指标，今天的行动只服务它。',
    缺少动力: '回忆最近完成的一个小胜利，复制那套开始方式。',
    缺少结构: '用 WBS 拆成 3 层，保留可执行的最底层行动。',
    被干扰: '记录干扰来源，设置 30 分钟后再处理的提醒。',
  }[blocker];

  const message = `
    <p><strong>${opener}</strong></p>
    <p>${toneText}</p>
    <p>${moodNudge}</p>
    <p>${blockerHint}</p>
    <p class="highlight">试试这个 life hack：${hack}</p>
  `;

  document.getElementById('interventionOutput').innerHTML = message;
}

function generateReflection(event) {
  event.preventDefault();
  const form = event.target;
  const quality = form.dayQuality.value;
  const highlight = form.highlight.value.trim();
  const block = form.block.value.trim();
  const experiment = form.experiment.value.trim();

  const nextStep = {
    一般: '明天挑 1 个最能改善节奏的动作，多做 10%。',
    优秀: '继续保持，并在日历中锁定两个深度工作块。',
    低迷: '先找回身心状态：早点睡、简单运动，再做 1 个小目标。',
  }[quality];

  const summary = `
    <p><strong>今天：</strong>${highlight}</p>
    <p><strong>阻碍：</strong>${block}</p>
    <p><strong>下一步实验：</strong>${experiment}</p>
    <p class="highlight">明日提示：${nextStep}</p>
  `;

  document.getElementById('reflectionOutput').innerHTML = summary;
}

function init() {
  const interventionForm = document.getElementById('interventionForm');
  const reflectionForm = document.getElementById('reflectionForm');
  interventionForm.addEventListener('submit', generateIntervention);
  reflectionForm.addEventListener('submit', generateReflection);

  // 预先生成一次默认提示
  interventionForm.dispatchEvent(new Event('submit'));
}

document.addEventListener('DOMContentLoaded', init);
