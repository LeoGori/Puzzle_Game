class Tile:
    def __init__(self, sprite):
        self.sprite = sprite
        self.pos = []

    def get_sprite(self):
        return self.sprite

    def set_right_pos(self, x, y):
        self.pos.append(x)
        self.pos.append(y)

    def get_pos_x(self):
        return self.pos[0]

    def get_pos_y(self):
        return self.pos[1]