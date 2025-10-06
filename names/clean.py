# lower_top100.py
# Переводит все строки в top-100.txt в нижний регистр

file_path = "top-100.txt"

with open(file_path, "r", encoding="utf-8") as f:
    lines = [line.strip().lower() for line in f if line.strip()]

with open(file_path, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

print(f"✅ Все {len(lines)} строк переведены в нижний регистр и сохранены в {file_path}")

