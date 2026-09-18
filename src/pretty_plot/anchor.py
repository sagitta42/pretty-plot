import enum


class ShiftType(int, enum.Enum):
    pad = 1
    move_out = -1


class AnchorPoint(enum.StrEnum):
    bottom_left = "bottom left"
    bottom_right = "bottom right"
    bottom_center = "bottom center"
    top_left = "top left"
    top_center = "top center"
    top_right = "top right"
    center_right = "center right"
    center_left = "center left"


class AnchorCoordinates(tuple, enum.Enum):
    bottom_left = (0, 0)
    bottom_right = (1, 0)
    bottom_center = (0.5, 0)
    top_left = (0, 1)
    top_right = (1, 1)
    top_center = (0.5, 1)
    center_right = (1, 0.5)
    center_left = (0, 0.5)

    def with_shift(
        self, shift_x: float, shift_y: float, how: ShiftType
    ) -> tuple[float, float]:
        """
        Get anchor point coordinates with shift for given shift type.

        how [ShiftType]: how the coordinates should be shifted relative to corner.
            pad: shift inwards
            move_out: shift outwards
        """
        ret = (
            self.value[0] + how.value * self._pad_sign(self.value[0]) * shift_x,
            self.value[1] + how.value * self._pad_sign(self.value[1]) * shift_y,
        )
        return ret

    @property
    def inverted(self) -> tuple[int, int]:
        if all(coord not in [0, 1] for coord in self.value):
            raise NotImplementedError(
                f"Cannot invert a non-edge anchor point {self.value}!"
            )
        ret = [(coord + 1) % 2 if coord in [0, 1] else coord for coord in self.value]
        return tuple(ret)

    def _pad_sign(self, coord: float) -> int:
        """
        Shift sign for padding given coordinate (moving inwards).
        """
        if coord == 0:
            return 1
        if coord == 1:
            return -1
        return 0

    @classmethod
    def from_anchor_point(cls, anchor_point: AnchorPoint):
        ret = cls[anchor_point.name]
        return ret
