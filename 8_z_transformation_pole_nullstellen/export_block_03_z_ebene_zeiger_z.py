from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "03_z_ebene_zeiger_z"
)

DPI = 200
FIGSIZE = (5.8, 5.2)
TITLE_SIZE = 22
LABEL_SIZE = 23
TICK_SIZE = 17
Z_LIMIT = 1.25

BLACK = "0.10"
GREY = "0.62"
LIGHT_GREY = "0.84"
SYSTEM_GREEN = "#26a043"
ANGLE = 0.25 * np.pi


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def clear_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()


def setup_z_axis(ax, title: str) -> None:
    theta = np.linspace(0.0, 2.0 * np.pi, 900)
    ax.plot(np.cos(theta), np.sin(theta), color=LIGHT_GREY, lw=2.4, zorder=1)
    ax.axhline(0.0, color=BLACK, lw=1.0, zorder=0)
    ax.axvline(0.0, color=BLACK, lw=1.0, zorder=0)
    ax.set_title(title, fontsize=TITLE_SIZE, pad=11)
    ax.set_xlim(-Z_LIMIT, Z_LIMIT)
    ax.set_ylim(-Z_LIMIT, Z_LIMIT)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel(r"Re$\{z\}$", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"Im$\{z\}$", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.20)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def draw_vector(
    ax,
    value: complex,
    *,
    color: str,
    label: str,
    alpha: float = 1.0,
    linewidth: float = 3.0,
    zorder: int = 4,
) -> None:
    ax.annotate(
        "",
        xy=(value.real, value.imag),
        xytext=(0.0, 0.0),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=linewidth,
            mutation_scale=18,
            alpha=alpha,
        ),
        zorder=zorder,
    )
    ax.scatter(
        [value.real],
        [value.imag],
        s=108,
        color=color,
        edgecolor="white",
        linewidth=1.1,
        alpha=alpha,
        zorder=zorder + 1,
    )
    ax.text(
        1.13 * value.real,
        1.13 * value.imag,
        label,
        color=color,
        fontsize=17,
        ha="left" if value.real >= 0 else "right",
        va="bottom" if value.imag >= 0 else "top",
        alpha=alpha,
        zorder=zorder + 2,
    )


def draw_angle_arc(
    ax,
    *,
    start_angle: float,
    end_angle: float,
    color: str,
    label: str,
    alpha: float = 1.0,
    zorder: int = 3,
) -> None:
    if np.isclose(start_angle, end_angle):
        return
    radius = 0.34
    theta = np.linspace(start_angle, end_angle, 90)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color=color, lw=2.2, alpha=alpha, zorder=zorder)
    ax.add_patch(
        FancyArrowPatch(
            (x[-2], y[-2]),
            (x[-1], y[-1]),
            arrowstyle="-|>",
            mutation_scale=14,
            color=color,
            lw=2.2,
            alpha=alpha,
            zorder=zorder + 1,
        )
    )
    label_angle = 0.5 * (start_angle + end_angle)
    ax.text(
        0.47 * np.cos(label_angle),
        0.47 * np.sin(label_angle),
        label,
        color=color,
        fontsize=15,
        ha="center",
        va="center",
        alpha=alpha,
        zorder=zorder + 2,
    )


def save_figure(fig, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


def export_empty_plane() -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor="white")
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.16, top=0.88)
    setup_z_axis(ax, "z-plane")
    save_figure(fig, "01_z_plane_unit_circle.png")


def export_z_vector() -> None:
    z = np.exp(1j * ANGLE)
    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor="white")
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.16, top=0.88)
    setup_z_axis(ax, "z-plane")
    draw_angle_arc(ax, start_angle=0.0, end_angle=ANGLE, color=BLACK, label=r"$\Omega$", zorder=3)
    draw_vector(ax, z, color=BLACK, label=r"$z=e^{j\Omega}$", zorder=4)
    save_figure(fig, "02_z_vector_r1_omega.png")


def export_inverse_vector() -> None:
    z = np.exp(1j * ANGLE)
    z_inverse = 1.0 / z
    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor="white")
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.16, top=0.88)
    setup_z_axis(ax, "z-plane")
    draw_angle_arc(ax, start_angle=0.0, end_angle=ANGLE, color=GREY, label=r"$\Omega$", alpha=0.62, zorder=2)
    draw_vector(
        ax,
        z,
        color=GREY,
        label=r"$z=e^{j\Omega}$",
        alpha=0.58,
        linewidth=2.6,
        zorder=3,
    )
    draw_vector(
        ax,
        z_inverse,
        color=SYSTEM_GREEN,
        label=r"$z^{-1}=e^{-j\Omega}$",
        alpha=1.0,
        linewidth=3.2,
        zorder=5,
    )
    save_figure(fig, "03_inverse_vector_z_minus_1.png")


def main() -> None:
    clear_output_dir()
    export_empty_plane()
    export_z_vector()
    export_inverse_vector()
    print(f"PNG figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
