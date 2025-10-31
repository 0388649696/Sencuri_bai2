# tamper bằng cách flip 1 bit trong file PDF đã ký
import sys
sys.stdout.reconfigure(encoding='utf-8')
import shutil
import os

SRC = r"D:\Apache24\anhtu\sencuri\pdf\signed.pdf"
DST = r"D:\Apache24\anhtu\sencuri\pdf\tampered.pdf"

# 1) copy file gốc -> file đích
shutil.copy2(SRC, DST)

# 2) flip 1 bit ở file đích (an toàn: tránh header PDF ở đầu)
with open(DST, "r+b") as f:
    data = bytearray(f.read())
    # chọn offset > 1024 để tránh header; nếu file nhỏ, đặt offset = len//2
    if len(data) < 2048:
        offset = max(256, len(data)//2)
    else:
        offset = 2000
    if offset >= len(data):
        offset = len(data) - 1
    data[offset] ^= 0x01  # flip bit
    f.seek(0)
    f.write(data)

print(f"Tạo xong: {DST} (byte flip tại offset {offset}).")
