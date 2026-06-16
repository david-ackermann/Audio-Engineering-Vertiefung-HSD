from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np


OUTPUT_ROOT = Path(__file__).resolve().parent / "png_storyboards"
BLOCK_DIR = OUTPUT_ROOT / "02_frequenzgang_iir" / "02B_iir_magnitude_examples"

DPI = 200
FIGSIZE = (11.5, 4.8)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 18

SIGNAL_BLACK = "0.10"
SYSTEM_GREEN = "#66b77a"
REFERENCE_GREY = "0.70"

FS_HZ = 48_000.0
NYQUIST_HZ = FS_HZ / 2.0
LOG_MIN_HZ = 20.0
GAIN_MINUS_3_DB = 10.0 ** (-3.0 / 20.0)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
    }
)


@dataclass(frozen=True)
class MagnitudeExample:
    slug: str
    title: str
    b0: float
    p: float
    coefficient_label: str = ""


EXAMPLES = (
    MagnitudeExample(
        slug="strong_low_frequency_emphasis",
        title=r"Strong LF emphasis",
        b0=0.15,
        p=0.85,
    ),
    MagnitudeExample(
        slug="mild_low_frequency_emphasis",
        title=r"Mild LF emphasis",
        b0=0.50,
        p=0.50,
    ),
    MagnitudeExample(
        slug="mild_high_frequency_emphasis",
        title=r"Mild HF emphasis",
        b0=0.50,
        p=-0.50,
    ),
    MagnitudeExample(
        slug="strong_high_frequency_emphasis",
        title=r"Strong HF emphasis",
        b0=0.15,
        p=-0.85,
    ),
)

MINUS_3_DB_EXAMPLES = tuple(
    MagnitudeExample(
        slug=f"{example.slug}_minus_3db",
        title=rf"{example.title} (-3 dB gain)",
        b0=example.b0 * GAIN_MINUS_3_DB,
        p=example.p,
        coefficient_label=rf"$b_0={example.b0 * GAIN_MINUS_3_DB:.3f}$, $p={example.p:+.2f}$",
    )
    for example in EXAMPLES
)


def clear_output_dir() -> None:
    BLOCK_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in BLOCK_DIR.rglob("*.png"):
        image_file.unlink()


def save_figure(fig, filename: str) -> None:
    fig.savefig(BLOCK_DIR / filename, dpi=DPI, facecolor="white", bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)


def response_from_frequency(frequency_hz: np.ndarray, b0: float, p: float) -> np.ndarray:
    omega = 2.0 * np.pi * frequency_hz / FS_HZ
    response = b0 / (1.0 - p * np.exp(-1j * omega))
    return response


def magnitude_db(response: np.ndarray) -> np.ndarray:
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def add_common_style(
    ax,
    example: MagnitudeExample,
    coefficient_x: float,
    coefficient_y: float,
) -> None:
    ax.set_title(
        rf"{example.title}",
        fontsize=TITLE_SIZE,
        pad=14,
    )
    coefficient_text = ax.text(
        coefficient_x,
        coefficient_y,
        example.coefficient_label or rf"$b_0={example.b0:.2f}$, $p={example.p:+.2f}$",
        transform=ax.transAxes,
        fontsize=20,
        color=SIGNAL_BLACK,
        ha="left",
        va="bottom",
    )
    coefficient_text.set_path_effects(
        [path_effects.withStroke(linewidth=4, foreground="white")]
    )
    ax.grid(alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=TICK_SIZE)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


def export_linear_magnitude_example(example: MagnitudeExample, filename: str) -> None:
    frequency_hz = np.linspace(0.0, NYQUIST_HZ, 4096)
    response = response_from_frequency(frequency_hz, example.b0, example.p)
    normalized_omega = frequency_hz / NYQUIST_HZ
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    ax.plot(normalized_omega, np.abs(response), color=SYSTEM_GREEN, lw=3.0)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_xlabel(r"Normalized angular frequency $\Omega/\pi$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude", fontsize=LABEL_SIZE)
    coefficient_x = 0.055 if example.p < 0.0 else 0.56
    coefficient_y = 0.78
    add_common_style(ax, example, coefficient_x, coefficient_y)
    save_figure(fig, filename)


def export_log_example(
    example: MagnitudeExample,
    filename: str,
    reference_example: MagnitudeExample | None = None,
) -> None:
    frequency_hz = np.logspace(np.log10(LOG_MIN_HZ), np.log10(NYQUIST_HZ), 4096)
    response = response_from_frequency(frequency_hz, example.b0, example.p)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.18, top=0.84)
    if reference_example is not None:
        reference_response = response_from_frequency(frequency_hz, reference_example.b0, reference_example.p)
        ax.plot(frequency_hz, magnitude_db(reference_response), color=REFERENCE_GREY, lw=3.0)
    ax.plot(frequency_hz, magnitude_db(response), color=SYSTEM_GREEN, lw=3.0)
    ax.set_xscale("log")
    ax.set_xlim(LOG_MIN_HZ, NYQUIST_HZ)
    ax.set_ylim(-30.0, 2.0)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax.set_yticks([-30, -24, -18, -12, -6, 0])
    ax.set_xlabel(r"Frequency in Hz, $f_s=48\,\mathrm{kHz}$", fontsize=LABEL_SIZE)
    ax.set_ylabel("Magnitude in dB", fontsize=LABEL_SIZE)
    coefficient_x = 0.055
    coefficient_y = 0.74 if example.p < 0.0 else 0.10
    add_common_style(ax, example, coefficient_x, coefficient_y)
    save_figure(fig, filename)


def main() -> None:
    clear_output_dir()
    for index, example in enumerate(EXAMPLES, start=1):
        linear_filename = f"{2 * index - 1:02d}_{example.slug}_linear_magnitude.png"
        log_filename = f"{2 * index:02d}_{example.slug}_log_db.png"
        export_linear_magnitude_example(example, linear_filename)
        export_log_example(example, log_filename)
    for offset, (example, reference_example) in enumerate(zip(MINUS_3_DB_EXAMPLES, EXAMPLES), start=9):
        export_log_example(example, f"{offset:02d}_{example.slug}_log_db.png", reference_example)
    print(f"PNG figures exported to: {BLOCK_DIR}")


if __name__ == "__main__":
    main()
