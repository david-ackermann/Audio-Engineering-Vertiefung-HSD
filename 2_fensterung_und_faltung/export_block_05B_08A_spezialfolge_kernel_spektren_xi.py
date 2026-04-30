from pathlib import Path
import importlib.util

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


CORE_SCRIPT = Path(__file__).resolve().parent / "export_block_05B_rueckweg_zur_faltung.py"
OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "png_storyboards"
    / "05_herleitung_und_dualitaet"
    / "05B_rueckweg_zur_faltung"
    / "08A_spezialfolge_kernel_spektren_xi"
)

INACTIVE_GREY = "0.52"


def load_core_module():
    spec = importlib.util.spec_from_file_location("block05b_core", CORE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = load_core_module()


def clear_outputs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_DIR.glob("*"):
        if path.is_file() and path.suffix.lower() == ".png":
            path.unlink()


def save_figure(fig, filename):
    fig.savefig(OUTPUT_DIR / filename, dpi=core.DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def shifted_window_spectrum_nu(freq_hz):
    return core.WINDOW_DURATION * core.np.sinc(core.WINDOW_DURATION * (core.FREQ_VALUES + freq_hz))


def kernel_label(freq_hz):
    return rf"$G_{{{core.frequency_label(freq_hz)}\,\mathrm{{Hz}}}}(\nu)$"


def export_kernel_sequence_figure(filename, kernels):
    fig, ax = core.create_figure(core.SPECTRUM_FIGSIZE)
    ax.plot(core.FREQ_VALUES, core.W_VALUES, color=core.WINDOW_GREEN, lw=1.9)

    legend_handles = [
        Line2D([0], [0], color=core.WINDOW_GREEN, lw=1.9, label=r"$W(\nu)$"),
    ]

    for freq_hz, color, linewidth, linestyle in kernels:
        ax.plot(core.FREQ_VALUES, shifted_window_spectrum_nu(freq_hz), color=color, lw=linewidth, ls=linestyle)
        legend_handles.append(
            Line2D([0], [0], color=color, lw=linewidth, ls=linestyle, label=kernel_label(freq_hz))
        )

    core.style_signed_frequency_axis(
        ax,
        r"Analysis kernel spectra $G_f(\nu)$",
        core.KERNEL_SPECTRUM_LIMIT,
        r"$G_f(\nu)$",
        x_label=r"Auxiliary frequency $\nu$ [Hz]",
    )
    core.add_inset_legend(ax, legend_handles, loc="upper left")
    save_figure(fig, filename)


def export_window_spectrum_nu_figure():
    fig, ax = core.create_figure(core.SPECTRUM_FIGSIZE)
    ax.plot(core.FREQ_VALUES, core.W_VALUES, color=core.WINDOW_GREEN, lw=2.4)
    core.style_signed_frequency_axis(
        ax,
        r"$G_f(\nu)=W(0-\nu)$",
        core.KERNEL_SPECTRUM_LIMIT,
        r"$W(\nu)$",
        x_label=r"Auxiliary frequency $\nu$ [Hz]",
    )
    core.add_inset_legend(
        ax,
        [Line2D([0], [0], color=core.WINDOW_GREEN, lw=2.4, label=r"$W(\nu)$")],
        loc="upper left",
    )
    save_figure(fig, "00_window_spectrum_nu_at_0hz.png")


def main():
    clear_outputs()
    core.configure_series(2.0, "2Hz")
    export_window_spectrum_nu_figure()

    export_kernel_sequence_figure(
        "01_kernel_spectrum_nu_red_at_2hz.png",
        [
            (2.0, core.ACTIVE_RED, 2.4, "-"),
        ],
    )
    export_kernel_sequence_figure(
        "02_kernel_spectrum_nu_grey_at_2hz.png",
        [
            (2.0, INACTIVE_GREY, 2.4, "-"),
        ],
    )
    export_kernel_sequence_figure(
        "03_kernel_spectrum_nu_red_at_0hz.png",
        [
            (2.0, INACTIVE_GREY, 2.0, "-"),
            (0.0, core.ACTIVE_RED, 2.4, "-"),
        ],
    )
    export_kernel_sequence_figure(
        "04_kernel_spectrum_nu_grey_at_0hz.png",
        [
            (2.0, INACTIVE_GREY, 2.0, "-"),
            (0.0, INACTIVE_GREY, 2.0, "--"),
        ],
    )
    export_kernel_sequence_figure(
        "05_kernel_spectrum_nu_red_at_minus5hz.png",
        [
            (2.0, INACTIVE_GREY, 2.0, "-"),
            (0.0, INACTIVE_GREY, 2.0, "--"),
            (-5.0, core.ACTIVE_RED, 2.4, "-"),
        ],
    )

    print(f"Special xi kernel figures exported to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
