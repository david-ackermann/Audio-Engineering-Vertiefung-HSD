from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "03_single_sideband_modulator" / "03a_single_sideband_material"

DPI = 200
FIGSIZE = (11.5, 4.8)
PHASOR_FIGSIZE = (11.5, 5.4)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18

CARRIER_FREQUENCY_HZ = 1_000.0
MODULATION_FREQUENCY_HZ = 200.0
DIFFERENCE_FREQUENCY_HZ = CARRIER_FREQUENCY_HZ - MODULATION_FREQUENCY_HZ
SUM_FREQUENCY_HZ = CARRIER_FREQUENCY_HZ + MODULATION_FREQUENCY_HZ

FREQUENCY_LIMIT_KHZ = 1.6
FREQUENCY_TICKS_KHZ = np.arange(-1.6, 1.6001, 0.4)
AMPLITUDE_LIMITS = (0.0, 1.0)
AMPLITUDE_TICKS = [0.0, 0.25, 0.5, 0.75, 1.0]

LEFT_GREEN = "#1f7a3f"
RIGHT_GREEN = "#66b77a"
REFERENCE_GREY = "0.72"
BLACK = "0.10"
PRODUCT_BLUE = "#2b7bbb"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


def style_spectrum_axis(ax_amplitude: plt.Axes, ax_phase: plt.Axes, title: str) -> None:
    ax_amplitude.set_title(title, fontsize=TITLE_SIZE, pad=14)
    ax_amplitude.set_xlim(-FREQUENCY_LIMIT_KHZ, FREQUENCY_LIMIT_KHZ)
    ax_amplitude.set_xticks(FREQUENCY_TICKS_KHZ)
    ax_amplitude.set_ylim(*AMPLITUDE_LIMITS)
    ax_amplitude.set_yticks(AMPLITUDE_TICKS)
    ax_amplitude.set_xlabel("Frequency in kHz", fontsize=LABEL_SIZE)
    ax_amplitude.set_ylabel("Component amplitude", fontsize=LABEL_SIZE)
    ax_amplitude.grid(alpha=0.30, which="major")
    ax_amplitude.set_axisbelow(True)
    ax_amplitude.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax_amplitude.spines[spine].set_visible(False)
    for spine in ax_amplitude.spines.values():
        spine.set_color(BLACK)

    ax_phase.set_ylim(-np.pi, np.pi)
    ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi])
    ax_phase.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax_phase.set_ylabel("Phase in rad", fontsize=LABEL_SIZE, labelpad=8)
    ax_phase.tick_params(labelsize=TICK_SIZE)
    ax_phase.spines["top"].set_visible(False)
    ax_phase.spines["left"].set_visible(False)
    ax_phase.spines["right"].set_color(BLACK)
    for phase_value in (-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi):
        ax_phase.axhline(
            phase_value,
            color=REFERENCE_GREY,
            lw=1.0,
            ls=":",
            alpha=0.40,
            zorder=0,
        )


def save_line_spectrum_with_phase(
    components: list[tuple[float, float, float]],
    *,
    title: str,
    filename: str,
) -> Path:
    frequencies_khz = np.array([frequency_hz / 1000.0 for frequency_hz, _, _ in components])
    amplitudes = np.array([amplitude for _, amplitude, _ in components])
    phases = np.array([phase for _, _, phase in components])

    fig, ax_amplitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    ax_phase = ax_amplitude.twinx()
    style_spectrum_axis(ax_amplitude, ax_phase, title)

    ax_amplitude.axhline(0.0, color=REFERENCE_GREY, lw=1.1, zorder=0)
    magnitude_lines = ax_amplitude.vlines(
        frequencies_khz,
        0.0,
        amplitudes,
        color=LEFT_GREEN,
        lw=3.6,
        zorder=3,
        label="Magnitude",
    )
    phase_lines = ax_phase.vlines(
        frequencies_khz,
        0.0,
        phases,
        color=RIGHT_GREEN,
        lw=1.9,
        ls="--",
        alpha=0.72,
        zorder=5,
    )
    phase_points = ax_phase.scatter(
        frequencies_khz,
        phases,
        color=RIGHT_GREEN,
        s=66,
        zorder=6,
        label="Phase",
    )

    legend = ax_amplitude.legend(
        [magnitude_lines, phase_points],
        ["Magnitude", "Phase"],
        loc="upper left",
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)

    fig.subplots_adjust(left=0.12, right=0.89, bottom=0.18, top=0.84)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def wrap_to_pi(angle: float) -> float:
    return (angle + np.pi) % (2.0 * np.pi) - np.pi


def style_phasor_axis(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=TITLE_SIZE, pad=12)
    ax.axhline(0.0, color=REFERENCE_GREY, lw=1.1, zorder=0)
    ax.axvline(0.0, color=REFERENCE_GREY, lw=1.1, zorder=0)
    unit_circle = plt.Circle((0.0, 0.0), 1.0, color=REFERENCE_GREY, fill=False, ls=":", lw=1.1, alpha=0.55)
    ax.add_patch(unit_circle)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_xlabel("Real", fontsize=LABEL_SIZE)
    ax.set_ylabel("Imaginary", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.22, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(BLACK)


def draw_phasor(
    ax: plt.Axes,
    *,
    angle: float,
    radius: float,
    color: str,
    label: str,
    label_offset: tuple[float, float] = (0.0, 0.0),
    lw: float = 3.0,
    zorder: int = 3,
) -> None:
    x_end = radius * np.cos(angle)
    y_end = radius * np.sin(angle)
    ax.annotate(
        "",
        xy=(x_end, y_end),
        xytext=(0.0, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0),
        zorder=zorder,
    )
    label_x = 1.08 * x_end + label_offset[0]
    label_y = 1.08 * y_end + label_offset[1]
    ax.text(
        label_x,
        label_y,
        label,
        color=color,
        fontsize=15,
        ha="center",
        va="center",
        zorder=zorder + 1,
    )


def save_product_phasor_diagram(
    *,
    title: str,
    filename: str,
    panels: list[dict[str, object]],
) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=PHASOR_FIGSIZE, dpi=DPI, facecolor="white")
    fig.suptitle(title, fontsize=TITLE_SIZE + 4, y=0.98)

    for ax, panel in zip(axes, panels):
        style_phasor_axis(ax, str(panel["title"]))
        for phasor in panel["phasors"]:
            draw_phasor(ax, **phasor)
        ax.text(
            -1.08,
            1.12,
            str(panel["formula"]),
            color=BLACK,
            fontsize=14,
            ha="left",
            va="center",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=2.0),
        )

    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.16, top=0.83, wspace=0.30)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    return path


def save_direct_product_phasors() -> Path:
    zero = 0.0
    panels = [
        {
            "title": r"Difference component $f_x-f_m$",
            "formula": r"$0+0=0$",
            "phasors": [
                {
                    "angle": zero,
                    "radius": 1.00,
                    "color": LEFT_GREEN,
                    "label": r"$X_+$",
                    "label_offset": (0.00, 0.12),
                },
                {
                    "angle": zero,
                    "radius": 0.78,
                    "color": RIGHT_GREEN,
                    "label": r"$M_-$",
                    "label_offset": (0.00, 0.00),
                },
                {
                    "angle": zero,
                    "radius": 0.56,
                    "color": PRODUCT_BLUE,
                    "label": r"$X_+M_-$",
                    "label_offset": (0.00, -0.12),
                },
            ],
        },
        {
            "title": r"Sum component $f_x+f_m$",
            "formula": r"$0+0=0$",
            "phasors": [
                {
                    "angle": zero,
                    "radius": 1.00,
                    "color": LEFT_GREEN,
                    "label": r"$X_+$",
                    "label_offset": (0.00, 0.12),
                },
                {
                    "angle": zero,
                    "radius": 0.78,
                    "color": RIGHT_GREEN,
                    "label": r"$M_+$",
                    "label_offset": (0.00, 0.00),
                },
                {
                    "angle": zero,
                    "radius": 0.56,
                    "color": PRODUCT_BLUE,
                    "label": r"$X_+M_+$",
                    "label_offset": (0.00, -0.12),
                },
            ],
        },
    ]
    return save_product_phasor_diagram(
        title=r"Direct product phasors: $\cos(\omega_x t)\cos(\omega_m t)$",
        filename="27_direct_product_phasor_diagram.png",
        panels=panels,
    )


def save_quadrature_product_phasors() -> Path:
    minus_half_pi = -0.5 * np.pi
    plus_half_pi = 0.5 * np.pi
    sum_phase = wrap_to_pi(minus_half_pi + minus_half_pi)
    panels = [
        {
            "title": r"Difference component $f_x-f_m$",
            "formula": r"$-\pi/2+\pi/2=0$",
            "phasors": [
                {
                    "angle": minus_half_pi,
                    "radius": 1.00,
                    "color": LEFT_GREEN,
                    "label": r"$\hat{X}_+$",
                    "label_offset": (-0.14, 0.00),
                },
                {
                    "angle": plus_half_pi,
                    "radius": 0.78,
                    "color": RIGHT_GREEN,
                    "label": r"$M_-$",
                    "label_offset": (0.12, 0.00),
                },
                {
                    "angle": 0.0,
                    "radius": 0.62,
                    "color": PRODUCT_BLUE,
                    "label": r"$\hat{X}_+M_-$",
                    "label_offset": (0.10, 0.04),
                },
            ],
        },
        {
            "title": r"Sum component $f_x+f_m$",
            "formula": r"$-\pi/2-\pi/2=-\pi$",
            "phasors": [
                {
                    "angle": minus_half_pi,
                    "radius": 1.00,
                    "color": LEFT_GREEN,
                    "label": r"$\hat{X}_+$",
                    "label_offset": (-0.14, 0.00),
                },
                {
                    "angle": minus_half_pi,
                    "radius": 0.78,
                    "color": RIGHT_GREEN,
                    "label": r"$M_+$",
                    "label_offset": (0.12, 0.00),
                },
                {
                    "angle": sum_phase,
                    "radius": 0.62,
                    "color": PRODUCT_BLUE,
                    "label": r"$\hat{X}_+M_+$",
                    "label_offset": (-0.06, 0.12),
                },
            ],
        },
    ]
    return save_product_phasor_diagram(
        title=r"Quadrature product phasors: $\sin(\omega_x t)\sin(\omega_m t)$",
        filename="28_quadrature_product_phasor_diagram.png",
        panels=panels,
    )


def direct_product_components() -> list[tuple[float, float, float]]:
    # cos(w_c n) cos(w_m n) = 0.5 cos((w_c-w_m)n) + 0.5 cos((w_c+w_m)n)
    return [
        (-SUM_FREQUENCY_HZ, 0.25, 0.0),
        (-DIFFERENCE_FREQUENCY_HZ, 0.25, 0.0),
        (DIFFERENCE_FREQUENCY_HZ, 0.25, 0.0),
        (SUM_FREQUENCY_HZ, 0.25, 0.0),
    ]


def quadrature_product_components() -> list[tuple[float, float, float]]:
    # sin(w_c n) sin(w_m n) = 0.5 cos((w_c-w_m)n) - 0.5 cos((w_c+w_m)n)
    return [
        (-SUM_FREQUENCY_HZ, 0.25, -np.pi),
        (-DIFFERENCE_FREQUENCY_HZ, 0.25, 0.0),
        (DIFFERENCE_FREQUENCY_HZ, 0.25, 0.0),
        (SUM_FREQUENCY_HZ, 0.25, np.pi),
    ]


def usb_components() -> list[tuple[float, float, float]]:
    # cos(w_c n) cos(w_m n) - sin(w_c n) sin(w_m n) = cos((w_c+w_m)n)
    return [
        (-SUM_FREQUENCY_HZ, 0.5, 0.0),
        (SUM_FREQUENCY_HZ, 0.5, 0.0),
    ]


def lsb_components() -> list[tuple[float, float, float]]:
    # cos(w_c n) cos(w_m n) + sin(w_c n) sin(w_m n) = cos((w_c-w_m)n)
    return [
        (-DIFFERENCE_FREQUENCY_HZ, 0.5, 0.0),
        (DIFFERENCE_FREQUENCY_HZ, 0.5, 0.0),
    ]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_paths = [
        save_line_spectrum_with_phase(
            direct_product_components(),
            title="Direct product spectrum",
            filename="21_direct_product_spectrum_magnitude_phase.png",
        ),
        save_line_spectrum_with_phase(
            quadrature_product_components(),
            title="Quadrature product spectrum",
            filename="22_quadrature_product_spectrum_magnitude_phase.png",
        ),
        save_line_spectrum_with_phase(
            usb_components(),
            title="USB spectrum",
            filename="23_usb_sine_spectrum_magnitude_phase.png",
        ),
        save_line_spectrum_with_phase(
            lsb_components(),
            title="LSB spectrum",
            filename="24_lsb_sine_spectrum_magnitude_phase.png",
        ),
    ]

    for path in image_paths:
        print(path)


if __name__ == "__main__":
    main()
