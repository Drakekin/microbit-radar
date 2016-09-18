import random

import microbit

BLANK_IMAGE = "00000:00000:00000:00000:00000"


def start_up(wait=1000):
    initial_ident = 0
    loading_display = microbit.Image(BLANK_IMAGE)
    for pixel in range(25):
        message = radio.receive_bytes



def get_line(start, end):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


class MicrobitImage:
    def __init__(self):
        self.image = microbit.Image(BLANK_IMAGE)

    def set_pixel(self, x, y, intensity):
        return self.image.set_pixel(x, y, intensity)

    def get_pixel(self, x, y):
        return self.image.get_pixel(x, y)

    def draw_line(self, x0, y0, x1, y1, intensity):
        line = get_line((x0, y0), (x1, y1))
        for x, y in line:
            self.set_pixel(x, y, intensity)
        return line

    def add(self, image):
        for x in range(5):
            for y in range(5):
                self.set_pixel(x, y, max(self.get_pixel(x, y), image.get_pixel(x, y)))

    def show(self):
        microbit.display.show(self.image)

    def decay(self, amount):
        for x in range(5):
            for y in range(5):
                self.set_pixel(x, y, max(0, self.get_pixel(x, y) - amount))

    def clone(self):
        image = MicrobitImage()
        image.image = self.image.copy()
        return image


if __name__ == "__main__":
    edges = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (3, 4),
        (2, 4),
        (1, 4),
        (0, 4),
        (0, 3),
        (0, 2),
        (0, 1),
    ]

    pings = [
        (4, 4),
        (0, 3),
        (1, 2),
        (3, 3)
    ]

    last_image = None
    n = 0
    ping_image = MicrobitImage()
    while True:
        for x, y in edges:
            n += 1

            image = MicrobitImage()
            pixels = image.draw_line(2, 2, x, y, 6)

            px = random.randint(0, 4)
            py = random.randint(0, 4)
            if (px, py) in pixels and not (px == 0 and py == 0):
                ping_image.set_pixel(px, py, 9)

            if n % 4 == 0:
                ping_image.decay(1)

            if last_image:
                image.add(last_image)
            last_image = image.clone()
            last_image.decay(1)
            image.add(ping_image)
            image.show()
