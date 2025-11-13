#!/usr/bin/env python3
"""重命名 flask-demo1 为 test 并更新所有相关配置"""

import os
import shutil
from pathlib import Path

def main():
    base_dir = Path("/Users/lingk/work/py/demo")
    old_name = "flask-demo1"
    new_name = "test"

    old_path = base_dir / old_name
    new_path = base_dir / new_name

    # 检查源目录是否存在
    if not old_path.exists():
        print(f"❌ 源目录不存在: {old_path}")
        return

    # 检查目标目录是否已存在
    if new_path.exists():
        print(f"❌ 目标目录已存在: {new_path}")
        print("请先删除或重命名现有的 test 目录")
        return

    # 重命名目录
    try:
        shutil.move(str(old_path), str(new_path))
        print(f"✅ 成功将 {old_name} 重命名为 {new_name}")
        print(f"   路径: {new_path}")
    except Exception as e:
        print(f"❌ 重命名失败: {e}")
        return

if __name__ == "__main__":
    main()

