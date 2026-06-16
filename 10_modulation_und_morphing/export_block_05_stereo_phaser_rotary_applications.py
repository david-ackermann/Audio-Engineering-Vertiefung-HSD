from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from PIL import Image


LECTURE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = LECTURE_DIR / "png_storyboards" / "05_applications_stereo_phaser_rotary" / "05a_stereo_phaser"

DPI = 200
FIGSIZE = (11.5, 4.8)
PHASOR_FIGSIZE = (6.4, 6.4)
TITLE_SIZE = 22
BUILD_TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18
TIME_LABEL_SIZE = 22

FS_HZ = 48_000.0
FREQUENCY_MIN_HZ = 20.0
FREQUENCY_MAX_HZ = 20_000.0
FREQUENCY_TICKS_HZ = [20.0, 50.0, 100.0, 200.0, 500.0, 1_000.0, 2_000.0, 5_000.0, 10_000.0, 20_000.0]
FREQUENCY_TICKLABELS = ["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"]
MAGNITUDE_LIMITS_DB = (-35.0, 5.0)
MAGNITUDE_TICKS_DB = [-35.0, -25.0, -15.0, -5.0, 5.0]

FRAME_COUNT = 88
FRAME_DURATION_MS = 80

STAGES = 6
D_GAIN = 0.5
E_GAIN = 0.5

COEF_0 = np.array(
    [
        0.036681502163648,
        0.274631759379454,
        0.561098969787919,
        0.769741833862266,
        0.892260818003879,
        0.962094548378084,
    ]
)
COEF_1 = np.array(
    [
        0.136547624631958,
        0.423138617436567,
        0.677540049974162,
        0.839889624849638,
        0.931541959963184,
        0.987816370732897,
    ]
)

LEFT_GREEN = "#1f7a3f"
RIGHT_GREEN = "#66b77a"
MODULATION_VIOLET = "#7b4ab8"
REFERENCE_GREY = "0.72"
BLACK = "0.10"
LIGHT_GREY = "0.86"
MARKER_RED = "tab:red"

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
    for gif_file in OUTPUT_DIR.glob("*.gif"):
        gif_file.unlink()


def frequency_grid() -> np.ndarray:
    return np.geomspace(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ, 4096)


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def phase_wrapped(response: np.ndarray) -> np.ndarray:
    return np.angle(response)


def allpass2_chain_response(frequencies_hz: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    omega = 2.0 * np.pi * frequencies_hz / FS_HZ
    z_inv_2 = np.exp(-2j * omega)
    response = np.ones_like(frequencies_hz, dtype=complex)
    for coefficient in coefficients:
        response *= (z_inv_2 - coefficient) / (1.0 - coefficient * z_inv_2)
    return response


def hilbert_pair_response(frequencies_hz: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    omega = 2.0 * np.pi * frequencies_hz / FS_HZ
    x_0 = allpass2_chain_response(frequencies_hz, COEF_0)
    x_90 = np.exp(-1j * omega) * allpass2_chain_response(frequencies_hz, COEF_1)
    return x_0, x_90


def ssb_stereo_phaser_response(
    frequencies_hz: np.ndarray,
    carrier_phase_rad: float,
) -> tuple[np.ndarray, np.ndarray]:
    x_0, x_90 = hilbert_pair_response(frequencies_hz)
    cos_m = np.cos(carrier_phase_rad)
    sin_m = np.sin(carrier_phase_rad)
    ssb_up = x_0 * cos_m - x_90 * sin_m
    ssb_down = x_0 * cos_m + x_90 * sin_m
    return D_GAIN + E_GAIN * ssb_up, D_GAIN + E_GAIN * ssb_down


def style_frequency_axis(ax: plt.Axes) -> None:
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_yticks(MAGNITUDE_TICKS_DB)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE, labelpad=10)
    ax.set_ylabel("|Y(f)/X(f)| in dB", fontsize=LABEL_SIZE, labelpad=12)
    ax.tick_params(axis="both", labelsize=TICK_SIZE, width=1.0, length=5)
    ax.grid(True, which="major", color="0.88", linewidth=1.0)
    ax.grid(True, which="minor", axis="x", color="0.94", linewidth=0.7)
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color(BLACK)


def style_build_frequency_axis(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=BUILD_TITLE_SIZE, pad=14)
    ax.set_xscale("log")
    ax.set_xlim(FREQUENCY_MIN_HZ, FREQUENCY_MAX_HZ)
    ax.set_xticks(FREQUENCY_TICKS_HZ)
    ax.set_xticklabels(FREQUENCY_TICKLABELS)
    ax.set_ylim(*MAGNITUDE_LIMITS_DB)
    ax.set_yticks(MAGNITUDE_TICKS_DB)
    ax.set_xlabel("Frequency in Hz", fontsize=LABEL_SIZE)
    ax.set_ylabel(r"$|H(f)|$ in dB", fontsize=LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.grid(alpha=0.18, which="minor", ls=":")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def style_time_axis(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, fontsize=BUILD_TITLE_SIZE, pad=14)
    ax.set_xlim(0.0, 360.0)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xticks([0.0, 90.0, 180.0, 270.0, 360.0])
    ax.set_xticklabels(["0°", "90°", "180°", "270°", "360°"])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel("Oscillator phase", fontsize=TIME_LABEL_SIZE)
    ax.set_ylabel("Amplitude", fontsize=TIME_LABEL_SIZE)
    ax.grid(alpha=0.30, which="major")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def create_build_mag_phase_figure(title: str) -> tuple[plt.Figure, plt.Axes, plt.Axes]:
    fig, ax_magnitude = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax_phase = ax_magnitude.twinx()

    style_build_frequency_axis(ax_magnitude, title)
    ax_phase.set_ylim(-np.pi, np.pi)
    ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0.0, 0.5 * np.pi, np.pi])
    ax_phase.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax_phase.set_ylabel("Phase in rad", fontsize=LABEL_SIZE)
    ax_phase.tick_params(labelsize=TICK_SIZE)
    ax_phase.spines["top"].set_visible(False)
    for phase_value in (-0.5 * np.pi, 0.5 * np.pi):
        ax_phase.axhline(
            phase_value,
            color=REFERENCE_GREY,
            lw=1.25,
            ls=":",
            alpha=0.55,
            zorder=0,
        )
    return fig, ax_magnitude, ax_phase


def create_time_figure(title: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    style_time_axis(ax, title)
    return fig, ax


def save_tight_figure(fig: plt.Figure, filename: str) -> None:
    fig.savefig(OUTPUT_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)


def setup_phasor_axis(title: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=PHASOR_FIGSIZE, dpi=DPI, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.96, bottom=0.12, top=0.86)
    ax.set_title(title, fontsize=BUILD_TITLE_SIZE, pad=14)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_xlabel("Real", fontsize=TIME_LABEL_SIZE)
    ax.set_ylabel("Imaginary / quadrature", fontsize=TIME_LABEL_SIZE)
    ax.grid(alpha=0.28, which="major")
    ax.axhline(0.0, color="0.30", lw=1.2)
    ax.axvline(0.0, color="0.30", lw=1.2)
    circle = plt.Circle((0.0, 0.0), 1.0, color=LIGHT_GREY, fill=False, lw=1.5, ls=":")
    ax.add_patch(circle)
    ax.tick_params(labelsize=14)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return fig, ax


def draw_arrow(ax: plt.Axes, value: complex, color: str, label: str, *, lw: float = 3.0, alpha: float = 1.0) -> None:
    ax.annotate(
        "",
        xy=(value.real, value.imag),
        xytext=(0.0, 0.0),
        arrowprops={
            "arrowstyle": "->",
            "color": color,
            "lw": lw,
            "alpha": alpha,
            "shrinkA": 0,
            "shrinkB": 0,
        },
    )
    label_radius = 1.08
    angle = np.angle(value) if abs(value) > 1e-12 else 0.0
    ax.text(
        label_radius * np.cos(angle),
        label_radius * np.sin(angle),
        label,
        color=color,
        fontsize=14,
        ha="center",
        va="center",
        fontweight="bold",
    )


def render_hilbert_frequency_rotation(positive_frequency: bool) -> plt.Figure:
    phase_deg = 45.0
    phase_rad = np.deg2rad(phase_deg)
    source = np.exp(1j * phase_rad) if positive_frequency else np.exp(-1j * phase_rad)
    multiplier = -1j if positive_frequency else 1j
    rotated = multiplier * source
    sign_label = r"$+\omega$" if positive_frequency else r"$-\omega$"
    rotation_label = r"$\times(-j)$, -90°" if positive_frequency else r"$\times(+j)$, +90°"
    title = "Hilbert rotation for positive frequency" if positive_frequency else "Hilbert rotation for negative frequency"

    fig, ax = setup_phasor_axis(title)
    draw_arrow(ax, source, REFERENCE_GREY, rf"{sign_label} input", lw=2.6, alpha=0.9)
    draw_arrow(ax, rotated, LEFT_GREEN, rf"{sign_label} Hilbert")
    ax.text(
        0.04,
        0.08,
        rotation_label,
        transform=ax.transAxes,
        fontsize=15,
        color=LEFT_GREEN,
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
    )
    return fig


def save_phasor_images() -> None:
    save_tight_figure(
        render_hilbert_frequency_rotation(positive_frequency=True),
        "22_phasor_hilbert_positive_frequency.png",
    )
    save_tight_figure(
        render_hilbert_frequency_rotation(positive_frequency=False),
        "23_phasor_hilbert_negative_frequency.png",
    )


def plot_mag_phase(
    ax_magnitude: plt.Axes,
    ax_phase: plt.Axes,
    frequencies_hz: np.ndarray,
    response: np.ndarray,
    *,
    color: str,
    magnitude_label: str,
    phase_label: str,
    lw: float = 3.0,
    alpha: float = 1.0,
    zorder: int = 3,
) -> tuple[Line2D, Line2D]:
    magnitude_line = ax_magnitude.plot(
        frequencies_hz,
        magnitude_db(response),
        color=color,
        lw=lw,
        alpha=alpha,
        zorder=zorder,
    )[0]
    phase_line = ax_phase.plot(
        frequencies_hz,
        phase_wrapped(response),
        color=color,
        lw=lw,
        ls="--",
        alpha=alpha,
        zorder=zorder,
    )[0]
    magnitude_line.set_label(magnitude_label)
    phase_line.set_label(phase_label)
    return magnitude_line, phase_line


def add_build_legend(ax: plt.Axes, lines: list[Line2D]) -> None:
    legend = ax.legend(
        lines,
        [line.get_label() for line in lines],
        loc="lower right",
        ncol=1,
        fontsize=13,
        frameon=True,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)


def render_frame(frame_index: int) -> Image.Image:
    frequencies_hz = frequency_grid()
    phase = 2.0 * np.pi * frame_index / FRAME_COUNT
    response_l, response_r = ssb_stereo_phaser_response(frequencies_hz, phase)
    reference_l, _ = ssb_stereo_phaser_response(frequencies_hz, 0.0)
    response_l_db = magnitude_db(response_l)
    response_r_db = magnitude_db(response_r)
    response_reference_db = magnitude_db(reference_l)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(frequencies_hz, response_reference_db, color=REFERENCE_GREY, lw=1.8, zorder=1)
    ax.plot(frequencies_hz, response_l_db, color=LEFT_GREEN, lw=2.8, zorder=3)
    ax.plot(frequencies_hz, response_r_db, color=RIGHT_GREEN, lw=2.8, zorder=2)
    ax.set_title("SSB stereo phaser response", fontsize=TITLE_SIZE, pad=14)
    style_frequency_axis(ax)

    ax.text(
        0.025,
        0.08,
        "Y_L",
        color=LEFT_GREEN,
        fontsize=TICK_SIZE,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.105,
        0.08,
        "Y_R",
        color=RIGHT_GREEN,
        fontsize=TICK_SIZE,
        fontweight="bold",
        transform=ax.transAxes,
    )

    fig.subplots_adjust(left=0.10, right=0.98, bottom=0.18, top=0.86)
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=DPI, facecolor="white")
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def render_allpass_node(title: str, response: np.ndarray, color: str) -> plt.Figure:
    frequencies_hz = frequency_grid()
    fig, ax_magnitude, ax_phase = create_build_mag_phase_figure(title)
    lines = list(
        plot_mag_phase(
            ax_magnitude,
            ax_phase,
            frequencies_hz,
            response,
            color=color,
            magnitude_label="Magnitude",
            phase_label="Phase",
        )
    )
    add_build_legend(ax_magnitude, lines)
    return fig


def render_quadrature_pair() -> plt.Figure:
    frequencies_hz = frequency_grid()
    x_0, x_90 = hilbert_pair_response(frequencies_hz)
    fig, ax_magnitude, ax_phase = create_build_mag_phase_figure("All-pass quadrature pair")
    lines: list[Line2D] = []
    lines.extend(
        plot_mag_phase(
            ax_magnitude,
            ax_phase,
            frequencies_hz,
            x_0,
            color=REFERENCE_GREY,
            magnitude_label=r"Magnitude $x_0$",
            phase_label=r"Phase $x_0$",
            lw=2.4,
            alpha=0.80,
            zorder=1,
        )
    )
    lines.extend(
        plot_mag_phase(
            ax_magnitude,
            ax_phase,
            frequencies_hz,
            x_90,
            color=LEFT_GREEN,
            magnitude_label=r"Magnitude $x_{90}$",
            phase_label=r"Phase $x_{90}$",
            zorder=3,
        )
    )
    add_build_legend(ax_magnitude, lines)
    return fig


def render_modulator_pair(phase_deg: float) -> plt.Figure:
    oscillator_phase_deg = np.linspace(0.0, 360.0, 1200)
    oscillator_phase_rad = np.deg2rad(oscillator_phase_deg)
    freeze_phase_rad = np.deg2rad(phase_deg)
    cos_signal = np.cos(oscillator_phase_rad)
    sin_signal = np.sin(oscillator_phase_rad)
    freeze_cos = np.cos(freeze_phase_rad)
    freeze_sin = np.sin(freeze_phase_rad)

    fig, ax = create_time_figure(rf"Quadrature modulator, cos phase {phase_deg:.0f}°")
    cos_line = ax.plot(
        oscillator_phase_deg,
        cos_signal,
        color=LEFT_GREEN,
        lw=3.0,
        label=r"$\cos(\omega_m n)$",
    )[0]
    sin_line = ax.plot(
        oscillator_phase_deg,
        sin_signal,
        color=RIGHT_GREEN,
        lw=3.0,
        ls="--",
        label=r"$\sin(\omega_m n)$",
    )[0]
    ax.axvline(phase_deg, color=REFERENCE_GREY, lw=1.8, ls=":", zorder=0)
    ax.scatter([phase_deg], [freeze_cos], color=LEFT_GREEN, s=75, zorder=5)
    ax.scatter([phase_deg], [freeze_sin], color=RIGHT_GREEN, s=75, zorder=5)
    ax.text(
        0.025,
        0.08,
        rf"$\cos={freeze_cos:.2f}$",
        transform=ax.transAxes,
        fontsize=15,
        color=LEFT_GREEN,
        fontweight="bold",
    )
    ax.text(
        0.18,
        0.08,
        rf"$\sin={freeze_sin:.2f}$",
        transform=ax.transAxes,
        fontsize=15,
        color=RIGHT_GREEN,
        fontweight="bold",
    )
    legend = ax.legend(
        [cos_line, sin_line],
        [cos_line.get_label(), sin_line.get_label()],
        loc="lower right",
        fontsize=14,
    )
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)
    return fig


def render_cos_modulator_frame(frame_index: int) -> Image.Image:
    oscillator_phase_deg = np.linspace(0.0, 360.0, 1200)
    oscillator_phase_rad = np.deg2rad(oscillator_phase_deg)
    cos_signal = np.cos(oscillator_phase_rad)
    phase_deg = 360.0 * frame_index / FRAME_COUNT
    phase_rad = np.deg2rad(phase_deg)
    cos_value = np.cos(phase_rad)

    fig, ax = create_time_figure(r"Cosine modulator")
    line = ax.plot(
        oscillator_phase_deg,
        cos_signal,
        color=MODULATION_VIOLET,
        lw=3.0,
        label=r"$c[n]=\cos(\omega_m n)$",
    )[0]
    ax.axvline(phase_deg, color=MARKER_RED, lw=2.0, alpha=0.90, zorder=3)
    ax.scatter([phase_deg], [cos_value], color=MARKER_RED, s=70, zorder=5)
    ax.text(
        0.025,
        0.08,
        rf"$c[n]={cos_value:+.2f}$",
        transform=ax.transAxes,
        fontsize=15,
        color=MODULATION_VIOLET,
        fontweight="bold",
    )
    legend = ax.legend([line], [line.get_label()], loc="lower right", fontsize=14)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("none")
    legend.get_frame().set_alpha(0.95)

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.035)
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def render_product_node(
    title: str,
    product_response: np.ndarray,
    reference_response: np.ndarray,
    *,
    color: str,
    product_label: str,
    reference_label: str,
) -> plt.Figure:
    frequencies_hz = frequency_grid()
    fig, ax_magnitude, ax_phase = create_build_mag_phase_figure(title)
    lines: list[Line2D] = []
    lines.extend(
        plot_mag_phase(
            ax_magnitude,
            ax_phase,
            frequencies_hz,
            reference_response,
            color=REFERENCE_GREY,
            magnitude_label=rf"Magnitude {reference_label}",
            phase_label=rf"Phase {reference_label}",
            lw=2.4,
            alpha=0.80,
            zorder=1,
        )
    )
    if np.max(np.abs(product_response)) < 1e-10:
        magnitude_line = ax_magnitude.plot(
            frequencies_hz,
            np.full_like(frequencies_hz, MAGNITUDE_LIMITS_DB[0]),
            color=color,
            lw=3.0,
            zorder=3,
            label=rf"Magnitude {product_label}",
        )[0]
        lines.append(magnitude_line)
        ax_magnitude.text(
            0.025,
            0.08,
            "muted product path; phase undefined",
            transform=ax_magnitude.transAxes,
            fontsize=14,
            color=color,
            fontweight="bold",
        )
    else:
        lines.extend(
            plot_mag_phase(
                ax_magnitude,
                ax_phase,
                frequencies_hz,
                product_response,
                color=color,
                magnitude_label=rf"Magnitude {product_label}",
                phase_label=rf"Phase {product_label}",
                zorder=3,
            )
        )
    add_build_legend(ax_magnitude, lines)
    return fig


def render_output_node(title: str, response: np.ndarray, reference: np.ndarray, color: str) -> plt.Figure:
    frequencies_hz = frequency_grid()
    fig, ax_magnitude, ax_phase = create_build_mag_phase_figure(title)
    lines: list[Line2D] = []
    lines.extend(
        plot_mag_phase(
            ax_magnitude,
            ax_phase,
            frequencies_hz,
            reference,
            color=REFERENCE_GREY,
            magnitude_label="Magnitude all-pass path",
            phase_label="Phase all-pass path",
            lw=2.4,
            alpha=0.80,
            zorder=1,
        )
    )
    lines.extend(
        plot_mag_phase(
            ax_magnitude,
            ax_phase,
            frequencies_hz,
            response,
            color=color,
            magnitude_label="Magnitude output",
            phase_label="Phase output",
            zorder=3,
        )
    )
    add_build_legend(ax_magnitude, lines)
    return fig


def save_build_up_images() -> None:
    frequencies_hz = frequency_grid()
    x_0, x_90 = hilbert_pair_response(frequencies_hz)

    save_tight_figure(
        render_allpass_node("After all-pass 1", x_0, LEFT_GREEN),
        "04_after_allpass_1_mag_phase.png",
    )
    save_tight_figure(
        render_allpass_node("After all-pass 2", x_90, LEFT_GREEN),
        "05_after_allpass_2_mag_phase.png",
    )
    save_tight_figure(
        render_quadrature_pair(),
        "06_allpass_quadrature_pair_cos1.png",
    )

    for phase_deg, filename_suffix in [(0.0, "cos1"), (45.0, "cos45"), (90.0, "cos90")]:
        phase = np.deg2rad(phase_deg)
        cos_m = np.cos(phase)
        sin_m = np.sin(phase)
        path_l = x_0 * cos_m - x_90 * sin_m
        path_r = x_0 * cos_m + x_90 * sin_m
        output_l = D_GAIN + E_GAIN * path_l
        output_r = D_GAIN + E_GAIN * path_r

        save_tight_figure(
            render_output_node(
                rf"$Y_L$ node, cos phase {phase_deg:.0f}°",
                output_l,
                path_l,
                LEFT_GREEN,
            ),
            f"{7 + int(phase_deg // 45) * 2:02d}_yl_{filename_suffix}_mag_phase.png",
        )
        save_tight_figure(
            render_output_node(
                rf"$Y_R$ node, cos phase {phase_deg:.0f}°",
                output_r,
                path_r,
                RIGHT_GREEN,
            ),
            f"{8 + int(phase_deg // 45) * 2:02d}_yr_{filename_suffix}_mag_phase.png",
        )

    for image_index, (phase_deg, filename_suffix) in enumerate(
        [(0.0, "cos0"), (45.0, "cos45"), (90.0, "cos90")],
        start=13,
    ):
        save_tight_figure(
            render_modulator_pair(phase_deg),
            f"{image_index:02d}_modulator_pair_{filename_suffix}.png",
        )

    product_image_index = 16
    for phase_deg, filename_suffix in [(0.0, "cos0"), (45.0, "cos45"), (90.0, "cos90")]:
        phase = np.deg2rad(phase_deg)
        cos_m = np.cos(phase)
        sin_m = np.sin(phase)
        product_x0 = x_0 * cos_m
        product_x90 = x_90 * sin_m

        save_tight_figure(
            render_product_node(
                rf"$x_0\cdot\cos$, cos phase {phase_deg:.0f}°",
                product_x0,
                x_0,
                color=LEFT_GREEN,
                product_label=r"$x_0\cdot\cos$",
                reference_label=r"$x_0$",
            ),
            f"{product_image_index:02d}_allpass1_times_cos_{filename_suffix}_mag_phase.png",
        )
        product_image_index += 1

        save_tight_figure(
            render_product_node(
                rf"$x_{{90}}\cdot\sin$, cos phase {phase_deg:.0f}°",
                product_x90,
                x_90,
                color=RIGHT_GREEN,
                product_label=r"$x_{90}\cdot\sin$",
                reference_label=r"$x_{90}$",
            ),
            f"{product_image_index:02d}_allpass2_times_sin_{filename_suffix}_mag_phase.png",
        )
        product_image_index += 1


def save_still() -> None:
    overlap_image = render_frame(0)
    offset_image = render_frame(FRAME_COUNT // 4)
    overlap_image.save(OUTPUT_DIR / "01_stereo_phaser_response_overlap_cos1.png")
    offset_image.save(OUTPUT_DIR / "02_stereo_phaser_response_stereo_offset.png")


def save_animation() -> None:
    frames = [render_frame(frame_index) for frame_index in range(FRAME_COUNT)]
    frames[0].save(
        OUTPUT_DIR / "03_stereo_phaser_response_sweep.gif",
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=False,
        disposal=2,
    )


def save_cos_modulator_animation() -> None:
    frames = [render_cos_modulator_frame(frame_index) for frame_index in range(FRAME_COUNT)]
    frames[0].save(OUTPUT_DIR / "24_cosine_modulator_start.png")
    frames[0].save(
        OUTPUT_DIR / "25_cosine_modulator_animation.gif",
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=False,
        disposal=2,
    )


def main() -> None:
    clear_output_dir()
    save_still()
    save_build_up_images()
    save_phasor_images()
    save_animation()
    save_cos_modulator_animation()
    print(f"Created stereo phaser storyboard in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
