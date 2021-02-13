class Tile:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.width = 64
        self.height = 64

        # offset the position from default position
        self.offset_x = 0
        self.offset_y = 0

    def get_image_path(self):
        return self.value + ".png"