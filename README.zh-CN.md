# 影视口述影像制作技能

简体中文 | [English](README.md)

这是一个交互式 Codex 技能，用于为短视频、动画和长篇电影制作可审阅的中文口述影像。

技能会先检查媒体，主动询问用户的口述密度、人物点名、自然语音和混音偏好；随后联合分析画面与声音、维护人物和剧情连续性，并生成带时间码的口述稿。用户没有明确批准当前口述稿以前，技能不会批量合成语音或混音成片。

## 主要功能

- 生成方便盲人用户审阅的中文带时间码口述稿
- 强制执行“先审稿、批准后再合成和混音”的制作流程
- 按场景切分长片，并利用子代理分批分析
- 让每条口述关联结构化画面观察与证据时间点，防止退化成剧情摘要
- 自动检查复述对白、画面覆盖稀疏、连续性资料缺失和长片后段偷懒漂移
- 依据片内证据确认角色身份，并提供有限时间内压缩文字和避让对白的详细规则
- 用户选择描述片头片尾后，强制覆盖公司 Logo、片名和所选演职员字幕
- 维护人物称呼、身份揭晓顺序、地点、物品和跨段剧情连续性
- 使用自然神经语音，按照实际可用时间动态调整语速
- 仅在口述实际发声期间压低原声；没有口述时保持影片原始音量
- 检查口述互相重叠、成片时长、音视频轨和媒体容器

## 环境要求

- 支持技能的 Codex
- Python 3.10 或更高版本
- `PATH` 中可用的 FFmpeg 和 FFprobe，用于媒体处理和成片检查
- 一个自然语音合成服务；工作流会推荐微软自然神经语音，但并不强制绑定某个供应商
- 可选的语音转写、镜头检测和视频分析工具，具体取决于制作环境

技能提供了一份非强制的[推荐工具链](references/recommended-tools.md)，包括 FFmpeg/FFprobe、Faster-Whisper、FFmpeg 镜头检测或 PySceneDetect、多模态视觉模型，以及 Microsoft Edge TTS。只要能够满足同样的时间戳、质量和验证要求，也可以换用其他本地、云端、商业或开源工具。

## 安装

### 让 Codex 自动安装

在 Codex 中输入：

```text
使用 $skill-installer 安装下面 GitHub 仓库中的技能，
并将技能命名为 film-audio-description：
https://github.com/wangru2025/film-audio-description-skill
```

安装后的技能会在下一轮对话中可用。

### 直接使用 Codex 自带的安装器

macOS 或 Linux：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo wangru2025/film-audio-description-skill \
  --path . \
  --name film-audio-description
```

Windows PowerShell：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" `
  --repo wangru2025/film-audio-description-skill `
  --path . `
  --name film-audio-description
```

为了避免意外覆盖，本安装器在目标目录已经存在时会停止。如果确实需要替换旧版本，请先自行备份、重命名或移除原来的 `film-audio-description` 技能目录。

### 手动安装

将仓库克隆到 Codex 技能目录：

```bash
git clone https://github.com/wangru2025/film-audio-description-skill.git \
  ~/.codex/skills/film-audio-description
```

Windows PowerShell：

```powershell
git clone https://github.com/wangru2025/film-audio-description-skill.git `
  "$env:USERPROFILE\.codex\skills\film-audio-description"
```

安装后请重启 Codex，或开始新一轮对话。

## 使用

显式调用技能：

```text
使用 $film-audio-description 为 D:\movie\电影.mp4 制作口述影像。
```

标准流程如下：

1. 检查影片时长、音频、视频和字幕轨。
2. 发起简短问卷，并为每项选择提供推荐值。
3. 先建立覆盖全片的场景表，再按场景分析通常 8–15 分钟的小段；约 20 分钟只用于组合审稿，不作为粗略分析单元。
4. 交付可读的带时间码口述稿和低置信度问题清单。
5. 等待用户修改和明确批准，例如回复 `Y`。
6. 合成自然语音、审计时间线、混音并验证最终成片。

## 重要制作规则

- 当前版本的口述稿必须由用户明确批准，之后才可批量生成语音或混音。
- 任何增加、删除或改变句意的修改都会使旧批准失效。
- 两条口述语音之间不得互相重叠。
- 常规口述必须关联具体画面观察和证据时间点；对白、转写、剧情简介和模型常识不能代替画面证据。
- 每个审稿批次交付前及整稿批准前，运行 `scripts/audit_project.py PROJECT_DIR`。
- 只有口述实际发声时，才能平滑、轻度压低影片原声。
- 没有口述时，无论原片中是对白、音乐、环境声、音效还是静音，原声增益都必须保持为 `1.0`。
- 成片先写入临时目标，检查成功后才成为正式输出文件。
- 用户应确保自己拥有处理和传播片源所需的权利或授权。

## 项目内容

- `SKILL.md`：技能入口和核心制作流程
- `references/`：问卷、写作规范、长片协作、项目格式和质量控制规则
- `scripts/init_project.py`：初始化标准口述影像项目
- `scripts/audit_cues.py`：审计口述时间线和语速
- `scripts/audit_project.py`：检查画面证据、场景覆盖、对白复述、连续性状态和长片质量漂移
- `scripts/verify_output.py`：检查成片时长、音视频轨和容器

## 许可证

MIT，详见 [LICENSE](LICENSE)。

当前版本：`v0.3.0`。
