from __future__ import annotations

class Vec2:

    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Vec2({self.x},{self.y})'

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}]'

    def apply(self, f) -> Vec2:
        return Vec2(f(self.x), f(self.y))

    def mul_cst(self, a) -> Vec2:
        return self.apply(lambda x: a * x)

    def add_vec2(self, v: Vec2) -> Vec2:
        return Vec2(self.x + v.x, self.y + v.y)

    def to_tuple(self) -> (float, float):
        return (self.x, self.y)


# v = Vec2(15, -15)
# a = Vec2(5, 5)

# print(f'v = {str(v)}')
# print(f'a = {str(a)}')

# print(f'v + a = {str(v.add_vec2(a))}')