import microbit
import radio
import random


DEFAULT_SETTINGS = {
    "length": 16,
    "queue": 128,
    "channel": 64,
    "data_rate": radio.RATE_2MBIT
}
BLANK_IMAGE = "00000:00000:00000:00000:00000"


def get_ident(wait=1000):
    max_ident = 0
    loading_display = microbit.Image(BLANK_IMAGE)
    wait /= 25

    configure_radio()
    for pixel in sorted(range(25), key=lambda x: random.random()):
        start = microbit.running_time()
        message = radio.receive_bytes()
        while message:
            try:
                sender, *_ = message
                max_ident = max(max_ident, sender)
            except ValueError:
                pass

            message = radio.receive_bytes()

        loading_display.set_pixel(pixel % 5, pixel // 5, 9)
        microbit.display.show(loading_display)
        end = microbit.running_time() - start
        if end < wait:
            microbit.sleep(wait - end)

    microbit.display.scroll("#{}".format(max_ident + 1))
    return max_ident + 1


def configure_radio(power=7):
    radio.config(power=power, **DEFAULT_SETTINGS)


def echolocate(me):
    configure_radio(7)
    radio.send_bytes(bytes([me, 255]))
    for power in range(8):
        configure_radio(power)
        radio.send_bytes(bytes([me, power]))

    microbit.sleep(10)

    message = radio.receive_bytes()
    while message:
        try:
            user, payload = message
            yield user, payload
        except ValueError:
            pass
        message = radio.receive_bytes()


if __name__ == "__main__":
    radio.on()

    while True:
        distance = {}

        ident = get_ident()
        duplicated = False

        while True:
            for user, packet in echolocate(ident):
                if user == ident:
                    duplicated = True
                    break

                if packet == 255:
                    if user in distance:
                        (n, p, l), _ = distance[user]
                        distance[user] = (9, n, p), microbit.running_time()
                    else:
                        distance[user] = (9, 9, 9), microbit.running_time()
                else:
                    if user in distance:
                        (n, p, l), _ = distance[user]
                        n = min(n, packet)
                        distance[user] = (n, p, l), microbit.running_time()

            if duplicated:
                microbit.sleep(random.randint(100, 5000))
                break

            bars = []

            now = microbit.running_time()

            for bit, ((n, p, l), seen) in sorted(distance.items(), key=lambda x: x[0]):
                if seen + 250 < now:
                    del distance[bit]
                    continue

                power = (n + p + l) // 3
                bar = "9" + "9" * min(4, power // 2) + "4" if power % 2 else ""
                bar += "0" * (5 - len(bar))
                bars.append(bar)

            for _ in range(5 - len(bars)):
                bars.append("".join(str(random.choice(range(4))) for _ in range(5)))

            microbit.display.show(microbit.Image(":".join(bars)))
