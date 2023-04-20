import math

def trilateration(p1, p2, p3, r1, r2, r3):
    '''三点定位算法'''
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = 2 * x2 - 2 * x1
    B = 2 * y2 - 2 * y1
    C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    D = 2 * x3 - 2 * x2
    E = 2 * y3 - 2 * y2
    F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)

    return x, y


def smooth_avg(xy_series, window_size=5):
    '''
    滑动平均算法
    xy_series: [(x1, y1), (x2, y2), ...]
    '''
    new_xy_series = []
    for idx in range(0, len(xy_series)):
        if idx <= window_size:
            window_size = idx
        elif idx >= len(xy_series) - window_size:
            window_size = len(xy_series) - idx - 1
        
        x = 0
        y = 0
        for i, xy in enumerate(xy_series[idx - window_size:idx + window_size + 1]):
            x += xy[0]
            y += xy[1]
        x = x / (2 * window_size + 1)
        y = y / (2 * window_size + 1)
        new_xy_series.append((x, y))
        
    return new_xy_series


