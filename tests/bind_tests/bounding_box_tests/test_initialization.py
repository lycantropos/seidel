from _seidel import (BoundingBox,
                     Point)


def test_basic() -> None:
    result = BoundingBox()

    assert result.empty is True
    assert result.lower == Point()
    assert result.upper == Point()
