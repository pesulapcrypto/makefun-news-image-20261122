"""THE MERIDIAN POST — @pesulapcrypto, Akun 12 — NI22 Wave 7.

Halaman ini menata kabar lintas zona waktu mengikuti garis meridian, dari Pasifik sampai Atlantik.
Tugas program di bawah sederhana: periksa keutuhan PNG, catat sidik
jarinya, lalu teruskan salinan persisnya ke direktori hasil.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

CONCEPT = "THE MERIDIAN POST"
ACCOUNT = "@pesulapcrypto"
ACCOUNT_LABEL = "Akun 12"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024


def abort(reason):
    sys.stderr.write(f"gagal: {reason}\n")
    sys.exit(1)


def run():
    folder = Path(__file__).resolve().parent
    picture = folder / "entry.png"
    if not picture.exists():
        abort("entry.png hilang dari folder repo")

    with picture.open("rb") as fh:
        head = fh.read(33)
    if len(head) != 33:
        abort("kepala berkas terlalu pendek untuk PNG yang sehat")
    if head[0:8] != b"\x89PNG\r\n\x1a\n":
        abort("tanda tangan PNG tidak cocok")
    if head[12:16] != b"IHDR":
        abort("IHDR tidak ditemukan")
    wide, tall = struct.unpack(">II", head[16:24])
    if wide > MAX_SIDE or tall > MAX_SIDE:
        abort(f"ukuran {wide}x{tall} melampaui pagar {MAX_SIDE} piksel")

    raw = picture.read_bytes()
    total = len(raw)
    fingerprint = hashlib.sha256(raw).hexdigest()

    dest_dir = Path(os.getenv("MAKEFUN_OUTPUT_DIR") or "/output")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    dest.write_bytes(raw)

    reread = dest.read_bytes()
    if len(reread) != total or hashlib.sha256(reread).hexdigest() != fingerprint:
        abort("hasil salinan berbeda dari aslinya")

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {total}")
    print(f"Dim: {wide}x{tall}")
    print(f"SHA256: {fingerprint}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(run())
