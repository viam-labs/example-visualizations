"""Color — RGB color helpers.

The wire format encodes color as ``{"r": int, "g": int, "b": int}``
with each channel in ``[0, 255]``. This module accepts the common
input shapes — dict, ``(r, g, b)`` tuple, or ``None`` — and
normalizes them so the rest of the library only ever sees the dict.
"""

from __future__ import annotations

from typing import Mapping, Optional, Tuple, Union


__all__ = ["ColorLike", "hsv_to_rgb", "normalize_color"]


ColorLike = Union[None, Mapping[str, int], Tuple[int, int, int]]


def normalize_color(c: ColorLike) -> Optional[Mapping[str, int]]:
    """Coerce a ColorLike into the wire-format dict.

    Accepts:
      * ``None`` → returns ``None`` (no color override)
      * ``{"r": int, "g": int, "b": int}`` → returned as-is (channel-typed)
      * ``(r, g, b)`` tuple or list → converted to dict

    Raises ``TypeError`` for anything else. Channel values are coerced
    to int but not range-clamped; callers responsible for staying in
    ``[0, 255]``.
    """
    if c is None:
        return None
    if isinstance(c, Mapping):
        return {"r": int(c["r"]), "g": int(c["g"]), "b": int(c["b"])}
    if isinstance(c, (tuple, list)) and len(c) == 3:
        return {"r": int(c[0]), "g": int(c[1]), "b": int(c[2])}
    raise TypeError(
        f"color must be None | dict | (r,g,b) tuple/list; got {type(c).__name__}"
    )


def hsv_to_rgb(h: float, s: float = 1.0, v: float = 1.0) -> Tuple[int, int, int]:
    """Convert HSV (each in ``[0, 1]``) to an 8-bit RGB tuple.

    Useful for animations that cycle through the rainbow. Hue wraps:
    ``hsv_to_rgb(1.5, 1, 1) == hsv_to_rgb(0.5, 1, 1)``.

    Example::

        # Cycle a sphere through the spectrum at 1 cycle per 5 seconds.
        sphere.color = viz.hsv_to_rgb((t / 5.0) % 1.0)
        return scene.update(sphere)
    """
    h6 = (h % 1.0) * 6.0
    i = int(h6) % 6
    f = h6 - int(h6)
    p, q, t_ = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    if i == 0:
        r, g, b = v, t_, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t_
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t_, p, v
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)
