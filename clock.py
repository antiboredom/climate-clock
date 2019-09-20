import argparse
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


START_DATE = datetime(2018, 1, 1, 2, 8, 6)  # estimated start date for the carbon budget
START_BUDGET = 420000000000.0
TONS_PER_SEC = 1331.0
PAUSE = 1.0 / 3.0  # framerate


def pluralize(text, num):
    """Pluralizes a string based on number value"""
    if num == 1:
        return text
    else:
        return text + "S"


def seconds_to_timestring(totalseconds):
    """Converts seconds to years/days/hours/minutes/seconds string"""
    years = divmod(totalseconds, 31540000)
    days = divmod(years[1], 60 * 60 * 24)
    hours = divmod(days[1], 60 * 60)
    minutes, seconds = divmod(hours[1], 60)

    years = int(years[0])
    days = int(days[0])
    hours = int(hours[0])
    minutes = int(minutes)
    seconds = int(seconds)

    return "{:01d}{} {:03d}{} {:02d}:{:02d}:{:02d}".format(
        years,
        pluralize("YR", years),
        days,
        pluralize("DAY", days),
        hours,
        minutes,
        seconds,
    )


def run(options):
    """run the countdown clock"""
    matrix = RGBMatrix(options=options)
    offscreen_canvas = matrix.CreateFrameCanvas()

    font = graphics.Font()
    font.LoadFont("rpi-rgb-led-matrix/fonts/9x18B.bdf")

    time_color = graphics.Color(255, 217, 25)
    co2_color = graphics.Color(153, 0, 230)

    while True:
        offscreen_canvas.Clear()

        # calculate remaining seconds and co2
        now = datetime.now()
        seconds_since_start = (now - START_DATE).total_seconds()
        remaining_co2 = START_BUDGET - seconds_since_start * TONS_PER_SEC
        remaining_seconds = remaining_co2 / TONS_PER_SEC

        # format text
        remaining_time_text = seconds_to_timestring(remaining_seconds)
        remaining_co2_text = "{:,} TONS".format(int(remaining_co2))

        # draw to screen
        graphics.DrawText(
            offscreen_canvas, font, 1, 14, time_color, remaining_time_text
        )
        graphics.DrawText(offscreen_canvas, font, 1, 28, co2_color, remaining_co2_text)

        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(PAUSE)


def main():
    parser = argparse.ArgumentParser()

    # arguments from the RGBMatrix library
    parser.add_argument(
        "-r",
        "--led-rows",
        action="store",
        help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32",
        default=32,
        type=int,
    )
    parser.add_argument(
        "--led-cols",
        action="store",
        help="Panel columns. Typically 32 or 64. (Default: 32)",
        default=32,
        type=int,
    )
    parser.add_argument(
        "-c",
        "--led-chain",
        action="store",
        help="Daisy-chained boards. Default: 1.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-P",
        "--led-parallel",
        action="store",
        help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--led-pwm-bits",
        action="store",
        help="Bits used for PWM. Something between 1..11. Default: 11",
        default=11,
        type=int,
    )
    parser.add_argument(
        "-b",
        "--led-brightness",
        action="store",
        help="Sets brightness level. Default: 100. Range: 1..100",
        default=100,
        type=int,
    )
    parser.add_argument(
        "-m",
        "--led-gpio-mapping",
        help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm",
        choices=["regular", "adafruit-hat", "adafruit-hat-pwm"],
        type=str,
    )
    parser.add_argument(
        "--led-scan-mode",
        action="store",
        help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)",
        default=1,
        choices=range(2),
        type=int,
    )
    parser.add_argument(
        "--led-pwm-lsb-nanoseconds",
        action="store",
        help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130",
        default=130,
        type=int,
    )
    parser.add_argument(
        "--led-show-refresh",
        action="store_true",
        help="Shows the current refresh rate of the LED panel",
    )
    parser.add_argument(
        "--led-slowdown-gpio",
        action="store",
        help="Slow down writing to GPIO. Range: 0..4. Default: 1",
        default=1,
        type=int,
    )
    parser.add_argument(
        "--led-no-hardware-pulse",
        action="store",
        help="Don't use hardware pin-pulse generation",
    )
    parser.add_argument(
        "--led-rgb-sequence",
        action="store",
        help="Switch if your matrix has led colors swapped. Default: RGB",
        default="RGB",
        type=str,
    )
    parser.add_argument(
        "--led-pixel-mapper",
        action="store",
        help='Apply pixel mappers. e.g "Rotate:90"',
        default="",
        type=str,
    )
    parser.add_argument(
        "--led-row-addr-type",
        action="store",
        help="0 = default; 1=AB-addressed panels;2=row direct",
        default=0,
        type=int,
        choices=[0, 1, 2],
    )
    parser.add_argument(
        "--led-multiplexing",
        action="store",
        help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0)",
        default=0,
        type=int,
    )

    args = parser.parse_args()

    options = RGBMatrixOptions()

    if args.led_gpio_mapping != None:
        options.hardware_mapping = args.led_gpio_mapping

    options.rows = args.led_rows
    options.cols = args.led_cols
    options.chain_length = args.led_chain
    options.parallel = args.led_parallel
    options.row_address_type = args.led_row_addr_type
    options.multiplexing = args.led_multiplexing
    options.pwm_bits = args.led_pwm_bits
    options.brightness = args.led_brightness
    options.pwm_lsb_nanoseconds = args.led_pwm_lsb_nanoseconds
    options.led_rgb_sequence = args.led_rgb_sequence
    options.pixel_mapper_config = args.led_pixel_mapper

    if args.led_show_refresh:
        options.show_refresh_rate = 1

    if args.led_slowdown_gpio != None:
        options.gpio_slowdown = args.led_slowdown_gpio

    if args.led_no_hardware_pulse:
        options.disable_hardware_pulsing = True

    try:
        print("Press CTRL-C to stop the clock")
        run(options)
    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
