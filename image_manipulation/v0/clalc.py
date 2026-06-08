
def calc_avg_color(src, origin: tuple[int, int], sides: tuple[int, int]) -> tuple[int, int, int]:
    x0, y0 = origin
    w, h = sides

    H, W = src.shape[:2]

    # Clamp region to image bounds
    x1 = max(0, x0)
    y1 = max(0, y0)
    x2 = min(W, x0 + w)
    y2 = min(H, y0 + h)

    roi = src[y1:y2, x1:x2]

    if roi.size == 0:
        return 0, 0, 0

    # OpenCV uses BGR
    r, g, b = roi.mean(axis=(0, 1))
    return round(float(r)), round(float(g)), round(float(b))


def avg_black_scale(src, origin: tuple[int, int], sides: tuple[int, int]) -> tuple[int, int, int]:
    avg_color = calc_avg_color(src=src,
                                    origin=origin,
                                    sides=sides)
    bgr_color = (avg_color[2], avg_color[1], avg_color[0])

    b = max(min(sum(bgr_color) // 3, 255), 0)
    return b, b, b

