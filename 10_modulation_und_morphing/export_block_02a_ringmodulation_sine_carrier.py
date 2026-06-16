from pathlib import Path

import numpy as np

import export_block_02d_am_modulation_sine_carrier as base


OUTPUT_DIR = base.LECTURE_DIR / "png_storyboards" / "02_am_modulation" / "02a_ringmodulation_sine_carrier"
RINGMOD_SINE_AMPLITUDE = 1.0
SINE_LINE_AMPLITUDE = 0.5
OUTPUT_COMPONENT_AMPLITUDE = 0.5 * RINGMOD_SINE_AMPLITUDE
OUTPUT_LINE_AMPLITUDE = 0.5 * OUTPUT_COMPONENT_AMPLITUDE
SPECTRUM_X_LIMIT_KHZ = 1.6
SPECTRUM_X_TICK_STEP_KHZ = 0.4


def main() -> None:
    base.OUTPUT_DIR = OUTPUT_DIR
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for image_file in OUTPUT_DIR.glob("*.png"):
        image_file.unlink()

    time_s = np.arange(int(round(base.DURATION_S * base.SAMPLE_RATE_HZ))) / base.SAMPLE_RATE_HZ
    carrier = np.sin(2.0 * np.pi * base.CARRIER_FREQUENCY_HZ * time_s)
    modulation_sine = np.sin(2.0 * np.pi * base.MODULATION_FREQUENCY_HZ * time_s)
    ringmod_gain = RINGMOD_SINE_AMPLITUDE * modulation_sine
    output = ringmod_gain * carrier

    difference_hz = base.CARRIER_FREQUENCY_HZ - base.MODULATION_FREQUENCY_HZ
    sum_hz = base.CARRIER_FREQUENCY_HZ + base.MODULATION_FREQUENCY_HZ

    image_paths = [
        base.save_time_signal(
            time_s,
            carrier,
            title="Carrier sine",
            color=base.SIGNAL_BLACK,
            filename="01_carrier_sine_time.png",
            y_limit=(-2.0, 2.0),
        ),
        base.save_line_spectrum(
            [
                (-base.CARRIER_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, base.SIGNAL_BLACK),
                (base.CARRIER_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, base.SIGNAL_BLACK),
            ],
            title="Carrier spectrum",
            filename="02_carrier_spectrum.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
        base.save_time_signal(
            time_s,
            modulation_sine,
            title="Modulation sine",
            color=base.MODULATION_VIOLET,
            filename="03_modulation_sine_time.png",
            y_limit=(-2.0, 2.0),
        ),
        base.save_line_spectrum(
            [
                (-base.MODULATION_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, base.MODULATION_VIOLET),
                (base.MODULATION_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, base.MODULATION_VIOLET),
            ],
            title="Modulation spectrum",
            filename="04_modulation_spectrum.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
        base.save_time_signal(
            time_s,
            ringmod_gain,
            title="Ringmod gain signal",
            color=base.MODULATION_VIOLET,
            filename="05_ringmod_gain_signal_time.png",
            y_limit=(-2.0, 2.0),
        ),
        base.save_line_spectrum(
            [
                (-base.MODULATION_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, base.MODULATION_VIOLET),
                (base.MODULATION_FREQUENCY_HZ, SINE_LINE_AMPLITUDE, base.MODULATION_VIOLET),
            ],
            title="Ringmod gain spectrum",
            filename="06_ringmod_gain_spectrum_no_dc.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
        base.save_time_signal(
            time_s,
            output,
            title="Ringmod output",
            color=base.SPECTRUM_BLUE,
            filename="07_ringmod_output_time.png",
            y_limit=(-2.0, 2.0),
        ),
        base.save_line_spectrum(
            [
                (-sum_hz, OUTPUT_LINE_AMPLITUDE, base.SPECTRUM_BLUE),
                (-difference_hz, OUTPUT_LINE_AMPLITUDE, base.SPECTRUM_BLUE),
                (difference_hz, OUTPUT_LINE_AMPLITUDE, base.SPECTRUM_BLUE),
                (sum_hz, OUTPUT_LINE_AMPLITUDE, base.SPECTRUM_BLUE),
            ],
            title="Output spectrum",
            filename="08_ringmod_output_spectrum_sidebands_only.png",
            x_limit_khz=SPECTRUM_X_LIMIT_KHZ,
            x_tick_step_khz=SPECTRUM_X_TICK_STEP_KHZ,
        ),
    ]

    for path in image_paths:
        print(path)


if __name__ == "__main__":
    main()
