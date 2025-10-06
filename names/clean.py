#!/usr/bin/env python3
# coding: utf-8
"""
Clean Uzbek name lists:
- normalize unicode
- map many apostrophe-like chars to ASCII "'"
- produce a version with only Latin letters (a-z) in lowercase
- if original contained "o'"-style, also produce variant with "o' -> u"
Input files: male_names.txt, female_names.txt
Output files: male_names_clean.txt, female_names_clean.txt
"""

import re
import unicodedata
from pathlib import Path

# апострофоподобные символы — все переводятся в ASCII-апостроф "'"
APOSTROPHE_CHARS = [
    "'", "’", "‘", "ʼ", "`", "´", "ʻ", "ʽ", "ʾ", "ʿ", "ˈ",
    "ˊ", "ˋ", "′", "‵", "ʹ",
    "\u02BB", "\u02BC", "\u02BD", "\u02BE", "\u02BF",
    "\u2018", "\u2019", "\u201B", "\u201A", "\u201C", "\u201D",
    "\u2032", "\u2035"
]
TRANS_TABLE = {ord(ch): "'" for ch in APOSTROPHE_CHARS}

# регулярка — оставить только латинские строчные буквы a-z
RE_NOT_ASCII_LETTERS = re.compile(r'[^a-z]')

def clean_file(input_path: str, output_path: str):
    inp = Path(input_path)
    if not inp.exists():
        print(f"Input file not found: {input_path}")
        return

    out_set = set()
    with inp.open("r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue

            # нормализация unicode и lowercase
            s = unicodedata.normalize("NFKC", s).lower()

            # заменить все апострофоподобные символы на обычный ASCII-апостроф
            s = s.translate(TRANS_TABLE)

            # вариант: удалить всё, кроме a-z
            name_alpha = RE_NOT_ASCII_LETTERS.sub("", s)
            if name_alpha:
                out_set.add(name_alpha)

            # если в исходнике встречается "o'" (после нормализации апострофы — уже '),
            # добавляем вариант с заменой o' -> u
            if "o'" in s:
                name_u_raw = s.replace("o'", "u")
                name_u = RE_NOT_ASCII_LETTERS.sub("", name_u_raw)
                if name_u:
                    out_set.add(name_u)

    out_list = sorted(out_set)
    with open(output_path, "w", encoding="utf-8") as wf:
        for name in out_list:
            wf.write(name + "\n")

    print(f"✅ {len(out_list)} unique names written to {output_path}")
    # небольшой сэмпл для проверки
    print("Sample:", out_list[:25])

if __name__ == "__main__":
    clean_file("male_names.txt", "male_names_clean.txt")
    clean_file("female_names.txt", "female_names_clean.txt")

    # Быстрая проверка на примерах:
    tests = [
        "annatug'on", "annatug‘on", "annatugʻon",
        "O'ktamjon", "O‘ktamjon", "Oʻktamjon",
        "Po'lat", "Po‘lat", "Poʻlat"
    ]
    print("\nQuick test results:")
    for t in tests:
        s = unicodedata.normalize("NFKC", t).lower().translate(TRANS_TABLE)
        alpha = RE_NOT_ASCII_LETTERS.sub("", s)
        u_variant = ""
        if "o'" in s:
            u_variant = RE_NOT_ASCII_LETTERS.sub("", s.replace("o'", "u"))
        print(f"{t!r} -> alpha: {alpha!r}" + (f", u: {u_variant!r}" if u_variant else ""))

