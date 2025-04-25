import numpy as np

# Определение функции и её градиента
# f(x, y) = 2x^2 + 4y^2 - 5xy + 11x + 8y - 3
# grad f = [4x - 5y + 11, 8y - 5x + 8]

def f(x):
    x_val, y_val = x
    return 2*x_val**2 + 4*y_val**2 - 5*x_val*y_val + 11*x_val + 8*y_val - 3

def grad_f(x):
    x_val, y_val = x
    df_dx = 4*x_val - 5*y_val + 11
    df_dy = 8*y_val - 5*x_val + 8
    return np.array([df_dx, df_dy])

# Метод покоординатного спуска
def coordinate_descent(x0, eps=1e-4, max_iter=10000):
    x = x0.copy()
    for k in range(max_iter):
        x_prev = x.copy()
        x[0] = (5*x[1] - 11) / 4
        x[1] = (5*x[0] - 8) / 8
        if np.linalg.norm(x - x_prev) < eps:
            break
    return x, k+1

# Метод градиентного спуска с фиксированным шагом
def gradient_descent(x0, alpha=0.01, eps=1e-4, max_iter=10000):
    x = x0.copy()
    for k in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < eps:
            break
        x = x - alpha * g
    return x, k+1

# Метод наискорейшего спуска (оптимальный шаг на каждой итерации)
def steepest_descent(x0, eps=1e-4, max_iter=10000):
    x = x0.copy()
    H = np.array([[4, -5],
                  [-5, 8]])
    for k in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < eps:
            break
        alpha_opt = (g @ g) / (g @ (H @ g))
        x = x - alpha_opt * g
    return x, k+1

if __name__ == "__main__":
    x0 = np.array([1.0, 1.0])
    eps = 1e-4

    x_cd, it_cd = coordinate_descent(x0, eps)
    x_gd, it_gd = gradient_descent(x0, alpha=0.01, eps=eps)
    x_sd, it_sd = steepest_descent(x0, eps)

    print("Исходная функция: f(x, y) = 2x^2 + 4y^2 - 5xy + 11x + 8y - 3\n")
    print("Метод покоординатного спуска:\n  x* =", x_cd, "за", it_cd, "итераций, f(x*) =", f(x_cd))
    print("\nМетод градиентного спуска (шаг = 0.01):\n  x* =", x_gd, "за", it_gd, "итераций, f(x*) =", f(x_gd))
    print("\nМетод наискорейшего спуска:\n  x* =", x_sd, "за", it_sd, "итераций, f(x*) =", f(x_sd))

