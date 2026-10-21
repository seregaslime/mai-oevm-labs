"""Рисует структурную схему ОЧ ЦП с вентилями и схему горизонтального микропрограммного УУ
для ЛР3 (ЛР №5 по методичке, вариант 7)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

plt.rcParams["font.family"] = "Arial"
IMG = os.path.join(os.path.dirname(__file__), "..", "img")
LW = 1.2

# Микропрограмма варианта 7 с совмещением: номера вентилей в каждой микрокоманде
MICROPROGRAM = [[1], [5], [2, 3], [7, 9], [5, 11], [6, 12], [5], [7, 8], [13], [14], [4]]
N_VENTS = 14
ADDR_BITS = 5


def box(ax, x0, y0, x1, y1, text="", fs=11):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, lw=LW))
    if text:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, text, ha="center", va="center", fontsize=fs)


def line(ax, pts, arrow=True):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="black", lw=LW, solid_capstyle="butt")
    if arrow:
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=LW,
                                    mutation_scale=12, shrinkA=0, shrinkB=0))


def vent(ax, x, y, n, r=0.2):
    ax.add_patch(Circle((x, y), r, facecolor="white", edgecolor="black", lw=LW, zorder=3))
    ax.text(x, y, f"V{n}", ha="center", va="center", fontsize=7.5, zorder=4)


def note(ax, x, y, text, **kw):
    ax.text(x, y, text, fontsize=8, style="italic", **kw)


def structure():
    fig, ax = plt.subplots(figsize=(11, 9.2))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0.5, 9.8)
    ax.axis("off")

    # ОП
    box(ax, 1.0, 8.2, 7.2, 9.6, "ЗМ (ZS)", fs=12)
    ax.text(1.1, 9.5, "ОП", fontsize=11, va="top")
    box(ax, 1.0, 7.0, 2.6, 7.5, "РАП (RAP)", fs=9)
    box(ax, 4.4, 7.0, 6.8, 7.5, "РЧП (RCH)", fs=9)
    line(ax, [(1.8, 7.5), (1.8, 8.2)])                                   # РАП -> ЗМ
    line(ax, [(5.4, 8.2), (5.4, 7.5)]); vent(ax, 5.4, 7.85, 5)           # чтение
    note(ax, 5.65, 7.85, "чт", ha="left", va="center")
    line(ax, [(4.8, 7.5), (4.8, 8.2)]); vent(ax, 4.8, 7.85, 4)           # запись
    note(ax, 4.55, 7.85, "зп", ha="right", va="center")

    # СК и РК
    box(ax, 1.0, 5.6, 2.6, 6.1, "СК (SK)", fs=9)
    line(ax, [(1.8, 6.1), (1.8, 7.0)]); vent(ax, 1.8, 6.55, 1)           # РАП:=СК
    line(ax, [(3.3, 5.85), (2.6, 5.85)]); vent(ax, 3.3, 5.85, 3)         # СК:=СК+1
    note(ax, 3.55, 5.85, "+1", va="center")
    box(ax, 4.2, 5.6, 4.9, 6.1, "КОП", fs=8)
    box(ax, 4.9, 5.6, 5.9, 6.1, "OP1", fs=8)
    box(ax, 5.9, 5.6, 6.9, 6.1, "OP2", fs=8)
    ax.text(7.0, 5.85, "РК", fontsize=10, va="center")
    line(ax, [(5.9, 7.0), (5.9, 6.1)]); vent(ax, 5.9, 6.55, 2)           # РК:=РЧП

    # OP1 -> РАП (V7)
    line(ax, [(5.4, 5.6), (5.4, 5.2), (0.55, 5.2), (0.55, 7.15), (1.0, 7.15)])
    vent(ax, 3.3, 5.2, 7)
    note(ax, 0.62, 6.2, "РК.OP1", rotation=90, va="center")

    # РАРП, РОН, РЧРП
    box(ax, 5.6, 3.8, 7.2, 4.3, "РАРП (RARP)", fs=8.5)
    line(ax, [(6.4, 5.6), (6.4, 4.3)]); vent(ax, 6.4, 4.95, 9)           # РАРП:=РК.OP2
    box(ax, 1.0, 1.9, 3.8, 4.3, "РОН (RON)", fs=12)
    line(ax, [(5.6, 4.05), (3.8, 4.05)])                                 # адрес РОН
    box(ax, 5.6, 1.9, 7.2, 2.4, "РЧРП (RCHR)", fs=8.5)
    line(ax, [(3.8, 2.65), (6.4, 2.65), (6.4, 2.4)]); vent(ax, 4.7, 2.65, 11)
    note(ax, 4.7, 2.9, "чт", ha="center")
    line(ax, [(5.6, 2.15), (3.8, 2.15)]); vent(ax, 4.7, 2.15, 10)
    note(ax, 4.7, 1.82, "зп", ha="center", va="top")

    # РЧРП -> РАП (V12)
    line(ax, [(6.4, 1.9), (6.4, 1.3), (0.3, 1.3), (0.3, 7.35), (1.0, 7.35)])
    vent(ax, 3.3, 1.3, 12)
    note(ax, 0.37, 4.0, "адрес 2-го операнда", rotation=90, va="center")

    # АЛУ
    box(ax, 8.0, 4.0, 9.2, 4.5, "RA")
    box(ax, 9.8, 4.0, 11.0, 4.5, "RB")
    ax.add_patch(Polygon([(7.8, 3.6), (9.35, 3.6), (9.5, 3.4), (9.65, 3.6), (11.2, 3.6),
                          (10.2, 2.6), (8.8, 2.6)], closed=True, fill=False, lw=LW))
    ax.text(9.5, 2.95, "АЛУ", ha="center", va="center", fontsize=10)
    line(ax, [(8.6, 4.0), (8.6, 3.6)])
    line(ax, [(10.4, 4.0), (10.4, 3.6)])
    box(ax, 8.9, 1.0, 10.1, 1.5, "RC")
    line(ax, [(9.5, 2.6), (9.5, 1.5)]); vent(ax, 9.5, 2.05, 13)          # RC:=RA+RB

    # РЧП -> RA (V6), RB (V8)
    line(ax, [(6.8, 7.25), (10.4, 7.25), (10.4, 4.5)])
    line(ax, [(8.6, 7.25), (8.6, 4.5)])
    ax.plot([8.6], [7.25], "ko", ms=3.5)
    vent(ax, 8.6, 5.8, 6)
    vent(ax, 10.4, 5.8, 8)

    # RC -> РЧП (V14)
    line(ax, [(10.1, 1.25), (11.7, 1.25), (11.7, 7.75), (6.4, 7.75), (6.4, 7.5)])
    vent(ax, 11.7, 4.5, 14)
    note(ax, 9.0, 7.85, "результат", va="bottom")

    fig.savefig(os.path.join(IMG, "рис_структурная_схема_ОЧ.png"), dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)


def control_unit():
    rows = len(MICROPROGRAM)
    dx, dy = 0.5, 0.42
    x0 = 2.2                                   # первая вертикальная шина V1
    xa0 = x0 + N_VENTS * dx + 0.5              # первая шина адресной части
    top = 1.0 + rows * dy                      # верхняя горизонтальная шина
    fig, ax = plt.subplots(figsize=(11, 7.6))
    ax.set_xlim(-0.2, xa0 + ADDR_BITS * dx + 0.6)
    ax.set_ylim(top - (rows - 1) * dy - 1.5, top + 2.1)
    ax.axis("off")

    ys = [top - i * dy for i in range(rows)]
    # РАМК и дешифратор
    box(ax, 0.0, top + 0.9, 1.3, top + 1.5, "РАМК", fs=10)
    box(ax, 0.3, ys[-1] - 0.3, 1.0, top + 0.3)
    ax.text(0.65, (ys[-1] + top) / 2, "Дешифратор адреса", rotation=90, ha="center",
            va="center", fontsize=10)
    line(ax, [(0.65, top + 0.9), (0.65, top + 0.3)])
    for i, y in enumerate(ys):
        ax.plot([1.0, xa0 + (ADDR_BITS - 1) * dx + 0.25], [y, y], color="black", lw=0.9)
        ax.text(1.1, y + 0.05, str(i), fontsize=7.5, va="bottom")
    # управляющая матрица
    for v in range(1, N_VENTS + 1):
        x = x0 + (v - 1) * dx
        ax.plot([x, x], [ys[-1] - 0.25, top + 0.35], color="black", lw=0.9)
        ax.text(x, top + 0.5, f"V{v}", ha="center", va="bottom", fontsize=8, rotation=90)
        line(ax, [(x, ys[-1] - 0.25), (x, ys[-1] - 0.75)])
    ax.text(x0 + (N_VENTS - 1) * dx / 2, top + 1.55, "Управляющая матрица (РМК)",
            ha="center", fontsize=10)
    ax.text(x0 + (N_VENTS - 1) * dx / 2, ys[-1] - 1.05,
            "к управляющим вентилям операционной части", ha="center", va="top", fontsize=9)
    for i, vents in enumerate(MICROPROGRAM):
        for v in vents:
            ax.plot([x0 + (v - 1) * dx], [ys[i]], "ko", ms=6)
    # адресная матрица: адрес следующей микрокоманды
    for b in range(ADDR_BITS):
        x = xa0 + b * dx
        ax.plot([x, x], [ys[-1] - 0.25, top + 0.35], color="black", lw=0.9)
        ax.text(x, top + 0.5, f"{2 ** (ADDR_BITS - 1 - b)}", ha="center", va="bottom", fontsize=8)
    ax.text(xa0 + (ADDR_BITS - 1) * dx / 2, top + 1.55, "Адрес след. МК", ha="center",
            fontsize=10)
    for i in range(rows):
        nxt = format(i + 1, f"0{ADDR_BITS}b")
        for b, bit in enumerate(nxt):
            if bit == "1":
                ax.plot([xa0 + b * dx], [ys[i]], "ko", ms=6)
    # обратная связь адресной части на РАМК
    xr = xa0 + (ADDR_BITS - 1) * dx
    line(ax, [(xr, ys[-1] - 0.25), (xr, ys[-1] - 0.55), (xr + 0.45, ys[-1] - 0.55),
              (xr + 0.45, top + 1.85), (0.65, top + 1.85), (0.65, top + 1.5)])

    fig.savefig(os.path.join(IMG, "рис_схема_УУ.png"), dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    structure()
    control_unit()
