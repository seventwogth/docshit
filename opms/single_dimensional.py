import math

def f(x):
    """Изначальная функция"""
    return math.sqrt(1 + x**2) - math.exp(-2 * x)


def df(x):
    """Первая производная"""
    return x / math.sqrt(1 + x**2) + 2 * math.exp(-2 * x)


def fdd(x):
    """Вторая производная"""
    return 1 / (1 + x**2)**1.5 - 4 * math.exp(-2 * x)


def bisection_method(fprime, a, b, eps):
    """
    Метод половинного деления
    """
    fa, fb = fprime(a), fprime(b)
    if fa * fb >= 0:
        raise ValueError("Производная имеет одинаковый знак на концах отрезка.")
    iterations = 0
    while (b - a) / 2 > eps:
        c = (a + b) / 2
        fc = fprime(c)
        if fa * fc <= 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        iterations += 1
    x = (a + b) / 2
    return x, f(x), iterations


def golden_section_method(func, a, b, eps):
    """
    Метод золотого сечения.
    """
    phi = (math.sqrt(5) - 1) / 2
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    iterations = 0
    while (b - a) > eps:
        if func(c) > func(d):
            a = c
            c = d
            d = a + phi * (b - a)
        else:
            b = d
            d = c
            c = b - phi * (b - a)
        iterations += 1
    x = (a + b) / 2
    return x, func(x), iterations


def chord_method(fprime, a, b, eps):
    """
    Метод хорд.
    """
    fa, fb = fprime(a), fprime(b)
    if fa * fb >= 0:
        raise ValueError("Производная имеет одинаковый знак на концах отрезка.")
    iterations = 0
    x = (a * fb - b * fa) / (fb - fa)
    while abs(fprime(x)) > eps:
        fx = fprime(x)
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        x = (a * fb - b * fa) / (fb - fa)
        iterations += 1
    return x, f(x), iterations


def newton_method(fprime, fdd, x0, eps, max_iter=100):
    """
    Метод Ньютона.
    """
    x = x0
    iterations = 0
    while abs(fprime(x)) > eps and iterations < max_iter:
        x = x - fprime(x) / fdd(x)
        iterations += 1
    return x, f(x), iterations

if __name__ == "__main__":
    a, b = 0.0, 1.0
    eps = 0.1

    menu = ("Выберите метод:\n"
            "1: Метод половинного деления\n"
            "2: Метод золотого сечения\n"
            "3: Метод хорд (секущих)\n"
            "4: Метод Ньютона\n")
    print(menu)
    choice = input("Введите номер метода (1-4): ")

    try:
        if choice == '1':
            x, fx, it = bisection_method(df, a, b, eps)
            name = "Половинное деление"
        elif choice == '2':
            x, fx, it = golden_section_method(f, a, b, eps)
            name = "Золотое сечение"
        elif choice == '3':
            x, fx, it = chord_method(df, a, b, eps)
            name = "Хорды (секущие)"
        elif choice == '4':
            x0 = (a + b) / 2
            x, fx, it = newton_method(df, fdd, x0, eps)
            name = "Ньютон"
        else:
            raise ValueError("Неверный выбор метода.")

        print(f"{name}: x = {x:.6f}, f(x) = {fx:.6f}, итераций = {it}")
    except ValueError as e:
        print(f"Ошибка при вычислении: {e}")
