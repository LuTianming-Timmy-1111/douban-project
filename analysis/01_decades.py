import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "analysis" / "output"
FONT_PATH = BASE_DIR / "fonts" / "simhei.ttf"

DB_HOST = os.environ.get("DB_HOST", "172.17.0.1")
URL = (
    f"mysql+pymysql://root:{os.environ['MYSQL_ROOT_PASSWORD']}"
    f"@{DB_HOST}:3307/douban?charset=utf8mb4"
)


def setup_font():
    font_manager.fontManager.addfont(FONT_PATH)
    name = font_manager.FontProperties(fname=FONT_PATH).get_name()
    plt.rcParams["font.family"] = name


def load():
    engine = create_engine(URL)
    df = pd.read_sql("SELECT id, title, rating, `year` FROM movie_new", engine)
    print("读取", len(df), "部")
    return df


def plot(counts):
    ax = counts.plot(kind="bar", figsize=(10, 5))
    ax.bar_label(ax.containers[0])
    ax.margins(y=0.08)
    ax.set_xticklabels([f"{d}s" for d in counts.index], rotation=0)
    ax.set_title("豆瓣电影 Top250 各年代部数")
    ax.set_xlabel("年代")
    ax.set_ylabel("部数")
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / "01_decades.png"
    plt.savefig(path, dpi=100)
    print("保存", path)


def main():
    setup_font()
    df = load()
    df["decade"] = df["year"].astype(int) // 10 * 10
    counts = df["decade"].value_counts().sort_index()
    print(counts)
    plot(counts)


if __name__ == "__main__":
    main()

