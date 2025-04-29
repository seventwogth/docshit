import math


def f(x):
    """Целевая функция: f(x) = sqrt(1 + x^2) - exp(-2x)"""
    return math.sqrt(1 + x**2) - math.exp(-2*x)


def df(x):
    """Первая производная f'(x) = x/sqrt(1+x^2) + 2*exp(-2x)"""
    return x / math.sqrt(1 + x**2) + 2 * math.exp(-2*x)


def fdd(x):
    """Вторая производная f''(x) = 1/(1+x^2)**1.5 - 4*exp(-2x)"""
    return 1 / (1 + x**2)**1.5 - 4 * math.exp(-2*x)


def dichotomy_minimize(func, a, b, eps=1e-6, max_iter=100):
    """Метод половинного деления отрезка для поиска минимума func(x) на [a,b]"""
    for i in range(1, max_iter+1):
        if (b - a) <= 2 * eps:
            break
        x1 = (a + b - eps) / 2
        x2 = (a + b + eps) / 2
        y1, y2 = func(x1), func(x2)
        if y1 > y2:
            a = x1
        else:
            b = x2
    x = 0.5 * (a + b)
    return x, func(x), i


def secant_method(func, a, b, tol=1e-6, max_iter=100):
    """Метод секущих для поиска корня func(x)=0 с начальными a, b"""
    fa, fb = func(a), func(b)
    if abs(fa) < tol:
        return a, fa, 0
    if abs(fb) < tol:
        return b, fb, 0
    if fa * fb > 0:
        raise ValueError("Нет изменения знака: метод секущих неприменим.")
    x_prev, x_curr = a, b
    f_prev, f_curr = fa, fb
    for i in range(1, max_iter+1):
        x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        f_next = func(x_next)
        if abs(f_next) < tol or abs(x_next - x_curr) < tol:
            return x_next, f_next, i
        x_prev, f_prev = x_curr, f_curr
        x_curr, f_curr = x_next, f_next
    raise RuntimeError("Максимум итераций без сходимости.")


def newton_method(func, deriv2, x0, tol=1e-6, max_iter=100):
    """Метод Ньютона для поиска корня func(x)=0, используя вторую производную"""
    x = x0
    for i in range(1, max_iter+1):
        f_val = func(x)
        df2 = deriv2(x)
        if abs(f_val) < tol:
            return x, f_val, i-1
        if df2 == 0:
            raise ZeroDivisionError("f''(x) = 0: метод Ньютона неприменим.")
        x_next = x - f_val / df2
        if abs(x_next - x) < tol:
            return x_next, func(x_next), i
        x = x_next
    raise RuntimeError("Максимум итераций без сходимости.")


def golden_section_minimize(func, a, b, tol=1e-6, max_iter=100):
    """Метод золотого сечения для поиска минимума func(x) на [a, b]"""
    phi = (math.sqrt(5) - 1) / 2
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    fc, fd = func(c), func(d)
    for i in range(1, max_iter+1):
        if (b - a) < tol:
            x = 0.5 * (a + b)
            return x, func(x), i
        if fc > fd:
            a = c
            c, fc = d, fd
            d = a + phi * (b - a)
            fd = func(d)
        else:
            b = d
            d, fd = c, fc
            c = b - phi * (b - a)
            fc = func(c)
    x = 0.5 * (a + b)
    return x, func(x), max_iter

if __name__ == "__main__":
    a, b = 0, 1
    tol = 0.1
    results = []
    x_d, f_d, it_d = dichotomy_minimize(f, a, b, tol)
    try:
        x_sec, f_sec, it_sec = secant_method(df, a, b, tol)
    except Exception as e:
        x_sec, f_sec, it_sec = None, None, str(e)
    try:
        x_new, f_new, it_new = newton_method(df, fdd, 0.5*(a+b), tol)
    except Exception as e:
        x_new, f_new, it_new = None, None, str(e)
    x_gs, f_gs, it_gs = golden_section_minimize(f, a, b, tol)
    header = ['Интервал', 'Метод', 'x', 'f(x)', 'Итераций']
    print(f"{header[0]:<12} | {header[1]:<20} | {header[2]:<10} | {header[3]:<10} | {header[4]}")
    print('-'*80)
    rows = [
        ("[0, 1]", "Метод половинного деления", x_d, f_d, it_d),
        ("[0, 1]", "Секущие", x_sec, f_sec, it_sec),
        ("[0, 1]", "Ньютон", x_new, f_new, it_new),
        ("[0, 1]", "Золотое сечение", x_gs, f_gs, it_gs),
    ]
    for interval, method, x_val, f_val, it in rows:
        print(f"{interval:<12} | {method:<20} | {str(x_val):<10} | {str(f_val):<10} | {it}")
    print('-'*80)

