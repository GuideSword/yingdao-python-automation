# 按需参考：影刀运行与接入

## Python 模块和配置

影刀官方 Python 模块使用 `main(args)` 作为入口；可视化流程可通过“调用模块”接入。如果没有已验证的文件导入接口，可以提供完整模块，让用户创建一个 Python 模块后粘贴代码，再连接调用入口。只需少量接入步骤，业务逻辑不逐条拖拽。

模块编辑器里的“运行”、主流程里的“调用模块”和控制台运行应用是不同的入口。Python 模块跑通，不意味着空的可视化主流程已连接；交付时分别说明验证范围。

JSON 通常用作运行配置，不是已确认支持直接导入的节点图。安装包中的 `FlowTemplates/blank.zip` 是可用的源码骨架线索，但存在该文件不证明控制台能直接导入任意 ZIP。不要伪造 `.bot`，或随意构造未经验证的 `.flow.json` 和元数据。

官方文档：

- [Python 编码版使用说明](https://www.yingdao.com/yddoc/language/zh-cn/专题文档/如何使用python编码版/python编码版使用说明.html)
- [package 接口](https://www.yingdao.com/yddoc/language/zh-cn/接口文档/package.html)

按需读取本机对应版本的文档，不假定网上示例兼容当前版本。

## 网页表单输入

优先使用用户已有元素库或稳定的业务属性选择器，如 `data-rpa`；避免坐标录制和与布局强耦合的选择器。

本次 ERP 案例中，`input(..., simulative=False)` 没有正确生效：字段为空或框架状态未更新，登录报错；保持账号配置及点击代码不变，改为 `simulative=True` 后成功。**这是已复现的兼容问题，不代表所有版本及网站的非模拟输入都失败。**

对本机支持的 API，可以采用：

```python
control = browser.find_by_css('[data-rpa="username"]', timeout=10)
control.input(config["username"], simulative=True, append=False)
if control.get_value() != config["username"]:
    raise RuntimeError("用户名输入未匹配配置，停止提交")
```

密码也可只比较是否相等，绝不输出内容。值一致仍不能独立证明 Vue/React 已接收输入事件，应进一步检查实际登录结果。只改必要参数，观察最小用例结果，避免无证据地添加固定延时或反复提交。

等待页面明确状态或元素，设置有界超时；不要把正常校验错误归咎于 Python 逗号或空格。配置首尾空白应告知并核实；尤其不能擅自 `strip()` 密码改变其含义。

## Excel 结果隔离

本次实测发现：先获取工作表，再对工作簿“另存为”，旧工作表引用仍可能写入源文件。后来采用以下修复方式，但文件隔离改动未完成本机原生复测；使用时应验证目标版本。

```python
import shutil
from pathlib import Path
from uuid import uuid4

source = Path(config["input_file"]).resolve()
output_dir = Path(config["output_dir"]).resolve()
output_dir.mkdir(parents=True, exist_ok=True)
result = output_dir / f"{source.stem}-结果-{uuid4().hex[:12]}{source.suffix}"
shutil.copy2(source, result)
book = xbot.excel.open(str(result), kind="openpyxl")
sheet = book.get_sheet_by_name(config["sheet"])
# 之后只操作 result 对应的 book / sheet，并按当前版本文档保存和释放资源。
```

`kind="openpyxl"` 适合 `.xlsx` 文件读写，不能据此承诺保留所有宏、图表、公式计算或第三方功能。若需要 WPS / Office 的真实应用能力，选用已确认支持的后端，但仍通过脚本操作，不开启影刀设计器的 GUI 自动化。

运行前后检查源文件哈希；读取结果文件实际单元格验证状态和错误码，而非只读取内存计数。测试已有记录时使用独立样本或唯一业务编号，不自动重置 ERP 库存和订单来获得“成功”。

## CLI 与应用文件

如果存在官方 `shadowbot.shell-cli.exe`，只检查与任务有关的 `--help` 子命令，再使用确实可用的创建、保存或启动接口。不要猜测参数、请求路径或内部 RPC。帮助中出现一个命令，不代表当前账号状态、版本和权限允许执行。

CLI 返回未登录或不支持时，不读账号文件提取令牌、不另造登录接口、不转为界面点击。说明阻碍并交付已完成代码；仅在缺少必需信息时向用户请求该信息。

用户授权修改已有应用不意味着可覆盖其他应用。修改之前确认路径、实际调用关系和用户改动；必要时保留原文件副本。不要猜测加密流程文件的内容，也不要解密或替换用户原有流程。
