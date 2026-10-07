"""Рисует структурную схему ЦП и блок-схему микропрограммы для ЛР2 (вариант 7)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch

plt.rcParams["font.family"] = "Arial"
IMG = os.path.join(os.path.dirname(__file__), "..", "img")
LW = 1.2


def box(ax, x0, y0, x1, y1, text="", fs=11, vertical=False):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, lw=LW))
    if text:
        if vertical:
            text = "\n".join(text)
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, text, ha="center", va="center", fontsize=fs)


def line(ax, pts, arrow=True):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="black", lw=LW, solid_capstyle="butt")
    if arrow:
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=LW,
                                    mutation_scale=12, shrinkA=0, shrinkB=0))


def signal(ax, x, y, text, to_x):
    ax.add_patch(Circle((x, y), 0.22, fill=False, lw=LW))
    ax.text(x, y, text, ha="center", va="center", fontsize=8)
    line(ax, [(x - 0.22 if to_x < x else x + 0.22, y), (to_x, y)])


def label(ax, x, y, text, **kw):
    ax.text(x, y, text, fontsize=8.5, style="italic", **kw)


def structure():
    fig, ax = plt.subplots(figsize=(10, 8.4))
    ax.set_xlim(0, 11)
    ax.set_ylim(0.4, 9.6)
    ax.axis("off")

    # ОП: РАП, ЗМ, РЧП
    box(ax, 1.0, 6.0, 6.2, 9.2)
    ax.text(1.1, 9.0, "ОП", fontsize=11, va="top")
    box(ax, 1.3, 6.3, 1.9, 8.7, "РАП", vertical=True)
    box(ax, 2.7, 6.9, 4.5, 8.3, "ЗМ", fs=12)
    box(ax, 5.3, 6.3, 5.9, 8.7, "РЧП", vertical=True)
    signal(ax, 6.9, 8.8, "Чт", 6.2)
    signal(ax, 6.9, 8.25, "Зп", 6.2)

    # СК и РК
    box(ax, 1.0, 4.9, 2.2, 5.4, "СК")
    line(ax, [(1.6, 5.4), (1.6, 6.3)])
    box(ax, 3.0, 4.9, 3.9, 5.4, "КОП", fs=10)
    box(ax, 3.9, 4.9, 4.9, 5.4, "A1", fs=10)
    box(ax, 4.9, 4.9, 5.9, 5.4, "A2", fs=10)
    ax.text(6.0, 5.15, "РК", fontsize=11, va="center")
    line(ax, [(5.6, 6.3), (5.6, 5.8), (4.45, 5.8), (4.45, 5.4)])          # РЧП -> РК

    # A1 -> РАП (прямой адрес 1-го операнда и адрес записи результата)
    line(ax, [(4.4, 4.9), (4.4, 4.5), (0.6, 4.5), (0.6, 7.2), (1.3, 7.2)])
    label(ax, 0.68, 5.9, "РК(A1)", rotation=90, va="center")

    # РОНы, РАРП, РЧРП
    box(ax, 0.9, 2.3, 2.6, 3.6, "РОНы", fs=12)
    box(ax, 3.2, 3.55, 4.6, 4.0, "РАРП", fs=10)
    box(ax, 3.2, 2.55, 4.6, 3.0, "РЧРП", fs=10)
    line(ax, [(5.4, 4.9), (5.4, 3.775), (4.6, 3.775)])                     # A2 -> РАРП
    label(ax, 5.47, 4.3, "РК(A2)", va="center")
    line(ax, [(3.2, 3.775), (2.9, 3.775), (2.9, 3.35), (2.6, 3.35)])       # РАРП -> РОНы
    line(ax, [(2.6, 2.775), (3.2, 2.775)])                                 # РОНы -> РЧРП
    ax.add_patch(Circle((1.75, 4.05), 0.22, fill=False, lw=LW))
    ax.text(1.75, 4.05, "Чт", ha="center", va="center", fontsize=8)
    line(ax, [(1.75, 3.83), (1.75, 3.6)])
    # РЧРП -> РАП (адрес 2-го операнда из РОНа)
    line(ax, [(3.9, 2.55), (3.9, 1.9), (0.3, 1.9), (0.3, 7.8), (1.3, 7.8)])
    label(ax, 0.38, 3.9, "адрес 2-го операнда", rotation=90, va="center")

    # АЛУ
    box(ax, 6.7, 3.4, 7.7, 3.9, "RA")
    box(ax, 8.3, 3.4, 9.3, 3.9, "RB")
    ax.add_patch(Polygon([(6.5, 3.0), (7.85, 3.0), (8.0, 2.8), (8.15, 3.0), (9.5, 3.0),
                          (8.6, 2.2), (7.4, 2.2)], closed=True, fill=False, lw=LW))
    ax.text(8.0, 2.5, "АЛУ", ha="center", va="center", fontsize=10)
    line(ax, [(7.2, 3.4), (7.2, 3.0)])
    line(ax, [(8.8, 3.4), (8.8, 3.0)])
    box(ax, 7.5, 1.2, 8.5, 1.7, "RC")
    line(ax, [(8.0, 2.2), (8.0, 1.7)])

    # РЧП -> RA, RB (операнды из ОП)
    line(ax, [(5.9, 6.9), (9.9, 6.9), (9.9, 4.4)], arrow=False)
    line(ax, [(9.9, 4.4), (7.2, 4.4), (7.2, 3.9)])
    line(ax, [(8.8, 4.4), (8.8, 3.9)])
    ax.plot([8.8], [4.4], "ko", ms=3.5)
    label(ax, 7.0, 7.0, "операнды", va="bottom")

    # RC -> РЧП (запись результата на место 1-го операнда)
    line(ax, [(8.0, 1.2), (8.0, 0.8), (10.4, 0.8), (10.4, 7.7), (5.9, 7.7)])
    label(ax, 7.0, 7.8, "результат", va="bottom")

    fig.savefig(os.path.join(IMG, "рис_структурная_схема.png"), dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


def flowchart():
    steps = [
        ("term", "Начало", None),
        ("io", "Ввод СК\n(адрес команды в ОП)", None),
        ("proc", "РАП:=СК\nРЧП:=Чт(РАП)\nРК:=РЧП\nСК:=СК+1", "1 этап. Выбор команды\nиз памяти"),
        ("proc", "Дешифрация КОП\n(КОП=1 – сложение)", "2 этап. Дешифрация\nкода операции"),
        ("proc", "РАП:=РК(A1)\nРЧП:=Чт(РАП)\nRA:=РЧП", "3 этап. Выбор 1-го\nоперанда (прямая\nадресация)"),
        ("proc", "РАРП:=РК(A2)\nРЧРП:=Чт(РАРП)\nРАП:=РЧРП\nРЧП:=Чт(РАП)\nRB:=РЧП",
         "3 этап. Выбор 2-го\nоперанда (косвенно-\nрегистровая адресация)"),
        ("proc", "RC:=RA+RB", "4 этап. Выполнение\nоперации в АЛУ"),
        ("proc", "РАП:=РК(A1)\nРЧП:=RC\nЗп(РАП):=РЧП", "5 этап. Запись результата\nна место 1-го операнда"),
        ("term", "Конец", None),
    ]
    W, gap = 3.0, 0.45
    heights = [0.55 if k == "term" else 0.35 + 0.28 * t.count("\n") + 0.28 for k, t, _ in steps]
    total = sum(heights) + gap * (len(steps) - 1)
    fig, ax = plt.subplots(figsize=(7.5, total * 0.95))
    ax.set_xlim(-2.2, 5.6)
    ax.set_ylim(-0.1, total + 0.1)
    ax.axis("off")
    cx, y = 0.0, total
    for (kind, text, note), h in zip(steps, heights):
        y0 = y - h
        if kind == "term":
            ax.add_patch(FancyBboxPatch((cx - W / 2, y0), W, h,
                                        boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                        fill=False, lw=LW))
        elif kind == "io":
            s = 0.3
            ax.add_patch(Polygon([(cx - W / 2 + s, y), (cx + W / 2 + s, y),
                                  (cx + W / 2 - s, y0), (cx - W / 2 - s, y0)],
                                 closed=True, fill=False, lw=LW))
        else:
            ax.add_patch(Rectangle((cx - W / 2, y0), W, h, fill=False, lw=LW))
        ax.text(cx, y0 + h / 2, text, ha="center", va="center", fontsize=11, linespacing=1.35)
        if note:
            ax.plot([cx + W / 2, cx + W / 2 + 0.25], [y0 + h / 2] * 2, color="black", lw=0.8,
                    ls="--")
            ax.text(cx + W / 2 + 0.35, y0 + h / 2, note, va="center", fontsize=9.5,
                    style="italic")
        if y0 > 0.01:
            line(ax, [(cx, y0), (cx, y0 - gap)])
        y = y0 - gap
    fig.savefig(os.path.join(IMG, "рис_блок_схема.png"), dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    structure()
    flowchart()
