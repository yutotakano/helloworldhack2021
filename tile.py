class Tile:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.width = 64
        self.height = 64

        self.poof_sprite = 0

        if isinstance(self.value, str):
            self.kind = "op"
        else:
            self.kind = "num"

        # offset the position from default position
        self.offset_x = 0
        self.offset_y = 0

    def get_image_path(self):
        return "assets/" + self.type + ".png"

    def isEqTile(self): 
        if self.value == "=":
            return True
        else:
            return False
    def isOpTile(self):
        if self.value == "+" or self.value == "-":
            return True
        else:
            return False 
    def isNumTile(self):
        if self.kind == "num":
            return True
        else:
            return False

    def next_poof(self):
        self.poof_sprite += 1
    
    
    def get_poof_path(self):
        return "assets/poof_" + str(self.poof_sprite) + ".png"

