#!/usr/bin/env python3
"""
自动化脚本 >>> update base config with file-name
"""

import os
import shutil
from pathlib import Path
import re

def replace_in_file(file_path, replacements):
    """在文件中替换文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        for old, new in replacements:
            content = content.replace(old, new)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  处理文件失败 {file_path}: {e}")
        return False

def main():
    base_dir = Path("/Users/lingk/work/py/demo")
    old_name = "flask-demo1"
    new_name = "test"

    old_path = base_dir / old_name
    new_path = base_dir / new_name

    print("=" * 60)
    print("🔄 Flask项目重命名工具")
    print("=" * 60)
    print(f"源目录: {old_path}")
    print(f"目标目录: {new_path}")
    print()

    # 步骤 1: 检查目录
    print("📋 步骤 1/4: 检查目录...")
    if not old_path.exists():
        print(f"❌ 源目录不存在: {old_path}")
        return

    if new_path.exists() and new_path.is_dir() and list(new_path.iterdir()):
        print(f"❌ 目标目录已存在且不为空: {new_path}")
        print("   请先删除或重命名现有的 test 目录")
        return

    print("✅ 目录检查通过")
    print()

    # 步骤 2: 重命名目录
    print("📋 步骤 2/4: 重命名目录...")
    try:
        if new_path.exists():
            shutil.rmtree(new_path)
        shutil.move(str(old_path), str(new_path))
        print(f"✅ 成功将 {old_name} 重命名为 {new_name}")
    except Exception as e:
        print(f"❌ 重命名失败: {e}")
        return
    print()

    # 步骤 3: 更新文件内容
    print("📋 步骤 3/4: 更新文件中的路径引用...")

    replacements = [
        (f"/Users/lingk/work/py/demo/{old_name}", f"/Users/lingk/work/py/demo/{new_name}"),
        (f"{old_name}/", f"{new_name}/"),
        (f"# {old_name} -", f"# {new_name} -"),
    ]

    # 需要更新的文件列表
    files_to_update = [
        new_path / "启动命令.md",
        new_path / "环境变量配置说明.md",
        new_path / "重新创建虚拟环境.sh",
        new_path / "test_context.sh",
        new_path / "document" / "README.md",
        new_path / "document" / "Config.md",
        new_path / "document" / "IDE配置说明.md",
        new_path / "document" / "项目说明.md",
        new_path / "document" / "Blueprint蓝图使用手册.md",
        new_path / "document" / "虚拟环境故障排查.md",
        new_path / "document" / "改名后修复指南.md",
        new_path / "FIX-修复虚拟环境.md",
        new_path / "QUICKSTART.md",
        new_path / "SUMMARY.md",
    ]

    updated_count = 0
    for file_path in files_to_update:
        if file_path.exists():
            if replace_in_file(file_path, replacements):
                print(f"  ✅ 已更新: {file_path.name}")
                updated_count += 1
            else:
                print(f"  ⏭️  无需更新: {file_path.name}")
        else:
            print(f"  ⚠️  文件不存在: {file_path.name}")

    print(f"\n✅ 共更新了 {updated_count} 个文件")
    print()

    # 步骤 4: 更新虚拟环境
    print("📋 步骤 4/4: 检查虚拟环境...")
    venv_path = new_path / "venv"

    if venv_path.exists():
        # 检查 pyvenv.cfg 文件
        pyvenv_cfg = venv_path / "pyvenv.cfg"
        if pyvenv_cfg.exists():
            with open(pyvenv_cfg, 'r') as f:
                content = f.read()

            if old_name in content:
                print("⚠️  虚拟环境包含旧路径引用")
                print("   建议重新创建虚拟环境:")
                print(f"   cd {new_path}")
                print("   rm -rf venv")
                print("   python3 -m venv venv")
                print("   source venv/bin/activate")
                print("   pip install -r requirements.txt")
            else:
                print("✅ 虚拟环境路径正常")
        else:
            print("✅ 虚拟环境检查完成")
    else:
        print("⚠️  未找到虚拟环境目录")

    print()
    print("=" * 60)
    print("🎉 重命名完成!")
    print("=" * 60)
    print()
    print("📝 后续步骤:")
    print(f"1. cd {new_path}")
    print("2. source venv/bin/activate")
    print("3. python run.py")
    print()
    print("如果启动失败,请重新创建虚拟环境(参考上面的命令)")
    print()

if __name__ == "__main__":
    main()

