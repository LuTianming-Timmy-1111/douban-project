import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "analysis" / "output"
FONT_PATH = BASE_DIR / "fonts" / "simhei.ttf"

DB_HOST = os.environ.get("DB_HOST", "172.17.0.1")  # git-guard: allow
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
    df = pd.read_sql("SELECT m.title, m.rating, g.name AS genre FROM movie_new m JOIN movie_genre mg ON m.id = mg.movie_id JOIN genre g ON mg.genre_id = g.id", engine)
    print("读取", len(df), "行")
    return df


def plot(top):
    ax = top["count"].plot(kind="bar", figsize=(10, 5))
    labels = [f"{c}\n{a:.2f}分" for c, a in zip(top["count"], top["avg"])]
    ax.bar_label(ax.containers[0], labels=labels)
    ax.margins(y=0.15)
    ax.set_xticklabels(top.index, rotation=0)
    ax.set_title("豆瓣电影 Top250 部数前 10 的类型 (柱上：部数 / 平均分) ")
    ax.set_xlabel("类型")
    ax.set_ylabel("部数")
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / "02_genres.png"
    plt.savefig(path, dpi=100)
    print("保存", path)


def main():
    setup_font()
    df = load()
    g = df.groupby("genre").agg(count=("title", "size"), avg=("rating", "mean"))
    top = g.sort_values("count", ascending=False).head(10)
    print(top.round(2))
    plot(top)


if __name__ == "__main__":
    main()

