import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# CONFIGURATIONS
API_KEY = "YOUR API KEY HERE"  # https://console.cloud.google.com/apis/dashboard
CHANNEL_ID = "YOUR CHANNEL ID HERE"

# Set up where we'll be fetching data from
DATA_SOURCE = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
DATA_LOCATION = ["items"]  # JSON PATH TO DATA

# The current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]

matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    json_path=DATA_LOCATION,
    status_neopixel=board.NEOPIXEL,
)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(16, 16),
    text_color=0xFF9900,
    scrolling=True,
)
matrixportal.preload_font(b"$012345789")  # preload numbers

last_check = None

while True:
    if last_check is None or time.monotonic() > last_check + 180:
        try:
            subscriberCount = int(matrixportal.fetch()[
                                  0]["statistics"]["subscriberCount"])
            viewCount = int(matrixportal.fetch()[0]["statistics"]["viewCount"])
            # Formatter with commas
            displayString = f"Subs: {subscriberCount:,} - Views: {viewCount:,}"
            print("Response is", displayString)
            last_check = time.monotonic()
            matrixportal.set_text(displayString, 0)
        except (ValueError, RuntimeError) as e:
            print("Some error occured, retrying! -", e)
    matrixportal.scroll()
    time.sleep(0.03)
