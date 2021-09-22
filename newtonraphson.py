import numpy as np
import matplotlib.pyplot as plt


def function(x):
    y = x**2 + 4
    return y


def newton_raphson(func, guesses, *args):
    """Newton-Raphson method to minimize a function
        :param func: function to minimize
        :type func: function
        :param guesses: list of initial root guesses
        :return x: x value of minimum
        :return y: y value of minimum
    """
    roots = []

    for x1 in guesses:
        guess = x1
        n = 0
        change = 1

        while abs(change) >= 1e-6:
            prev = x1

            dx = -0.0001*x1
            x2 = x1 + dx

            # print(args)

            y1 = func(args[0][0], args[0][1], x1, args[0][2])
            y2 = func(args[0][0], args[0][1], x2, args[0][2])

            if len(y1) > 1:
                y1 = y1[0]

            if len(y2) > 1:
                y2 = y2[0]

            m = (y2 - y1)/dx
            x1 = (-y1/m) + x1

            # plt.plot([x1, prev], [0, y1], 'k--')

            change = x1 - prev
            n += 1

            # if n >= 100:
            if m <= 1e-3:
                print('Unable to converge for root: ' + str(guess) + ' but did find a min at: ' + str((x1, y1)))
                break

        roots.append(x1)

    return roots

