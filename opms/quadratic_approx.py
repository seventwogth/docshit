import math

def f(x):
    return math.sqrt(1 + x**2) - math.exp(-2 * x)

def quadratic_approximation(a, b, epsilon, mode='min'):
    c = (a + b) / 2
    fa = f(a)
    fb = f(b)
    fc = f(c)
    iterations = 0
    prev_a, prev_b = a, b
    
    while (b - a) > epsilon:
        denominator = ((c - b) * fa + (a - c) * fb + (b - a) * fc)
        if denominator == 0:
            c = (a + b) / 2
            fc = f(c)
            iterations += 1
            continue
        
        numerator = ((c**2 - b**2) * fa + (a**2 - c**2) * fb + (b**2 - a**2) * fc)
        x_star = 0.5 * numerator / denominator
        x_star_clamped = max(a, min(x_star, b))
        fx_star = f(x_star_clamped)
        
        points = [(a, fa), (b, fb), (c, fc)]
        reverse_sort = (mode == 'min')
        points.sort(key=lambda x: x[1], reverse=reverse_sort)
        worst_point, worst_value = points[0]
        
        if (mode == 'min' and fx_star < worst_value) or (mode == 'max' and fx_star > worst_value):
            if worst_point == a:
                a, fa = x_star_clamped, fx_star
            elif worst_point == b:
                b, fb = x_star_clamped, fx_star
            else:
                c, fc = x_star_clamped, fx_star
        else:
            c = (a + b) / 2
            fc = f(c)
        
        if a == prev_a and b == prev_b:
            break
        prev_a, prev_b = a, b
        
        iterations += 1
        if iterations > 1000:
            break
    
    fa_final = f(a)
    fb_final = f(b)
    if mode == 'min':
        return (a, fa_final) if fa_final < fb_final else (b, fb_final)
    else:
        return (a, fa_final) if fa_final > fb_final else (b, fb_final)

a, b = 0, 1
epsilon = 0.0001

min_point, min_value = quadratic_approximation(a, b, epsilon, 'min')
print(f"Минимум: x = {min_point:.5f}, f(x) = {min_value:.5f}")

max_point, max_value = quadratic_approximation(a, b, epsilon, 'max')
print(f"Максимум: x = {max_point:.5f}, f(x) = {max_value:.5f}")
