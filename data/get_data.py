"""Download the Rossmann Store Sales dataset (public Kaggle competition mirror).
Byte-identical to the files analyzed in this repo (md5-checked below).
Source: https://github.com/dmi3kno/Kaggle-Rossmann (mirror of the Kaggle
"Rossmann Store Sales" competition data). Kaggle competition data is shared
for non-commercial practice; we link and download rather than redistribute.
"""
import hashlib
import urllib.request
from pathlib import Path

FILES = {
    "rossmann_train.csv": (
        "https://raw.githubusercontent.com/dmi3kno/Kaggle-Rossmann/master/train.csv",
        "d47aedd9e2d580e06a6ef7ce1732e8b6",
    ),
    "rossmann_store.csv": (
        "https://raw.githubusercontent.com/dmi3kno/Kaggle-Rossmann/master/store.csv",
        "30c9ccb5af66c21f65e7d1da967e6251",
    ),
}

here = Path(__file__).resolve().parent
for name, (url, md5) in FILES.items():
    dest = here / name
    if dest.exists() and hashlib.md5(dest.read_bytes()).hexdigest() == md5:
        print(f"{name} already present"); continue
    print(f"downloading {name} ...")
    urllib.request.urlretrieve(url, dest)
    got = hashlib.md5(dest.read_bytes()).hexdigest()
    assert got == md5, f"checksum mismatch for {name}: {got}"
    print(f"{name} ok ({dest.stat().st_size:,} bytes)")
