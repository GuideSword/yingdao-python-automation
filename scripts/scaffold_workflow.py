"""Create source files for a Yingdao Python module, without operating Yingdao UI."""
import argparse
import json
import keyword
from pathlib import Path


MODULE = '''"""Yingdao Python module. Implement run(config) before delivering."""
import json
from collections.abc import Mapping
from pathlib import Path


def load_config(args):
    configured_path = args.get("config_path") if isinstance(args, Mapping) else None
    path = Path(configured_path) if configured_path else Path(__file__).with_name("__CONFIG_NAME__")
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(config, dict):
        raise ValueError("配置文件必须是 JSON 对象")
    return config


def run(config):
    # Implement the requested business workflow with the installed xbot SDK.
    # Keep passwords out of logs; verify real submission and output-file results.
    raise NotImplementedError("流程骨架尚未实现，请先编写业务逻辑")


def main(args):
    return run(load_config(args))
'''


def scaffold(output, name):
    if not name.isascii() or not name.isidentifier() or keyword.iskeyword(name):
        raise ValueError("模块名必须是非关键字的 ASCII Python 标识符")
    output = Path(output).expanduser().resolve()
    module_path = output / (name + ".py")
    config_path = output / (name + ".config.json")
    paths = (module_path, config_path)
    for path in paths:
        if path.exists():
            raise FileExistsError("拒绝覆盖已有文件：" + str(path))
    output.mkdir(parents=True, exist_ok=True)
    module_source = MODULE.replace("__CONFIG_NAME__", config_path.name)
    compile(module_source, str(module_path), "exec")
    # Exclusive creation also refuses files created between preflight and writing.
    with module_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(module_source)
    with config_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"schema_version": 1, "settings": {}}, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return {"module": str(module_path), "config": str(config_path),
            "status": "scaffold_only", "native_import_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="生成源码的目录")
    parser.add_argument("--name", default="workflow", help="模块文件名，不含 .py")
    args = parser.parse_args()
    try:
        result = scaffold(args.output, args.name)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
