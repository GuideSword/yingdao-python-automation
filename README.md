# 影刀 Python 自动化 · Codex Skill

让 Codex 使用 Python 模块、JSON 配置和已验证的 CLI/API 编写影刀自动化，减少拖拽搭建与反复操作设计器。

**默认不使用 Computer Use。只有用户明确指定时，才允许使用 Computer Use；也不换用其他 GUI 工具绕过这一限制。**

## 能做什么

- 创建、修改和排查影刀 `main(args)` Python 模块。
- 生成可复用源码骨架，并将运行参数与代码分开。
- 优先读取当前版本的接口文档，避免猜测 SDK 和导入格式。
- 区分代码检查、模块实跑、主流程连接和原生导入验证。
- 记录表单事件兼容及 Excel 回写隔离的实践经验。

本仓库提供的是 Codex 技能和源码骨架，不是可直接导入影刀的原生应用包。

## 安装

将仓库内容放入 Codex 的个人技能目录：

```powershell
git clone https://github.com/GuideSword/yingdao-python-automation.git "$env:USERPROFILE\.codex\skills\yingdao-python-automation"
```

如果该目录已经存在，请先检查现有内容，不要直接覆盖。

## 使用

在 Codex 中调用：

```text
$yingdao-python-automation 帮我创建一个读取 Excel 并录入 ERP 的影刀 Python 流程。
```

技能也允许自动匹配相关的影刀 Python 自动化任务。

生成模块骨架：

```powershell
python scripts/scaffold_workflow.py --output ./my-workflow --name orders
python -m py_compile ./my-workflow/orders.py
```

生成 `orders.py` 和 `orders.config.json`。骨架中的 `run(config)` 需要根据业务实现；未实现时会明确报错，不会假装已完成。

没有已验证的无界面接入能力时，Codex 应交付完整代码和最少人工接入步骤，并说明未验证的部分，不擅自开始操作影刀界面。

## 文件

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | Codex 的任务匹配说明和核心执行规则 |
| [agents/openai.yaml](agents/openai.yaml) | 技能显示信息与自动匹配设置 |
| [references/runtime-notes.md](references/runtime-notes.md) | 按需读取的影刀运行与接入说明 |
| [scripts/scaffold_workflow.py](scripts/scaffold_workflow.py) | 不操作 GUI 的 Python 模块骨架生成器 |

已验证技能结构、脚本生成、Python 语法、JSON 配置及拒绝覆盖现有文件的行为。骨架生成器不依赖影刀；真正的 `xbot` 业务流程需要影刀运行环境。
