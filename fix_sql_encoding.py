#!/usr/bin/env python3
"""检查 init_dmma_db.sql 编码，如果是 UTF-8 无 BOM 则确认通过；否则转为 UTF-8 无 BOM 重新保存。"""

import os

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init_dmma_db.sql")

def is_utf8_no_bom(data: bytes) -> bool:
    if data[:3] == b'\xef\xbb\xbf':
        return False
    try:
        data.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

with open(FILE_PATH, "rb") as f:
    raw = f.read()

if is_utf8_no_bom(raw):
    print(f"[OK] {FILE_PATH} 已经是 UTF-8 无 BOM 编码，无需处理。")
else:
    if raw[:3] == b'\xef\xbb\xbf':
        print("[FIX] 检测到 BOM 标记，正在移除并重新保存...")
        raw = raw[3:]
    else:
        print("[FIX] 文件不是有效 UTF-8，尝试用 GBK 解码后转 UTF-8...")
        text = raw.decode("gbk")
        raw = text.encode("utf-8")

    with open(FILE_PATH, "wb") as f:
        f.write(raw)
    print(f"[DONE] 已重新保存为 UTF-8 无 BOM 编码: {FILE_PATH}")
