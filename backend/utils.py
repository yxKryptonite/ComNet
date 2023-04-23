import pandas as pd
import matplotlib.pyplot as plt

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
    xy_series = pd.DataFrame(xy_series, columns=['x', 'y'])
    x, y = xy_series['x'], xy_series['y']
    new_x = x.rolling(window_size, min_periods=1).mean()
    new_y = y.rolling(window_size, min_periods=1).mean()
    new_xy_series = [(x, y) for x, y in zip(new_x, new_y)]
    return new_xy_series


if __name__ == "__main__":
    xy_series = []
    POINT_NUM = 20
    for i in range(POINT_NUM):
        x = i
        if i % 2 == 0:
            y = 0
        elif i % 4 == 3:
            y = 10
        else:
            y = -5
        xy_series.append((x, y))
    print(xy_series)
    new_xy_series = smooth_avg(xy_series, window_size=5)
    print(new_xy_series)
    plt.plot([xy[0] for xy in xy_series], [xy[1] for xy in xy_series], label='raw')
    plt.plot([xy[0] for xy in new_xy_series], [xy[1] for xy in new_xy_series], label='smooth')
    plt.show()