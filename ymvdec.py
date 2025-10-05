

import os
import sys

MAGIC_HEADER = bytes.fromhex("EF C9 ED F3 14 05 5C 51 51 5F")
WMV_MAGIC = bytes.fromhex("30 26 B2 75")

def decrypt_segment(segment: bytes) -> bytes:
    """对单个段进行解密，返回解密后的字节流。"""
    output = bytearray()
    for n, b in enumerate(segment):
        key = ((n & 0xF) + 0x10) & 0xFF
        decoded = b ^ key 
        output.append(decoded)
    return bytes(output)

def extract_file(input_file: str, output_dir: str):
    try:
        with open(input_file, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"[错误] 读取文件失败: {e}")
        return

    # 先判断是否为 WMV/ASF
    if data.startswith(WMV_MAGIC):
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(input_file))[0]
        out_path = os.path.join(output_dir, f"{base}.wmv")
        try:
            with open(out_path, "wb") as out:
                out.write(data)
            print(f"[OK] 检测到 WMV 文件，已输出到 {out_path} ({len(data)} 字节)")
        except Exception as e:
            print(f"[错误] 写 WMV 文件失败: {e}")
        return

    # 如果不是 WMV，按之前的方式处理 JPG 段
    parts = data.split(MAGIC_HEADER)
    if len(parts) <= 1:
        print("[错误] 文件中未找到任何有效段。")
        return

    # 丢弃第0段
    segments = parts[1:]
    os.makedirs(output_dir, exist_ok=True)

    for idx, seg in enumerate(segments, start=1):
        raw_segment = MAGIC_HEADER + seg
        decrypted = decrypt_segment(raw_segment)

        out_path = os.path.join(output_dir, f"output_{idx:03d}.jpg")
        try:
            with open(out_path, "wb") as out:
                out.write(decrypted)
            print(f"[OK] 写出 {out_path} ({len(decrypted)} 字节)")
        except Exception as e:
            print(f"[错误] 写文件失败 {out_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"用法: python {sys.argv[0]} <输入文件> <输出目录>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    extract_file(input_file, output_dir)

