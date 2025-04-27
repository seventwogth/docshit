import random

# Матрица расстояний между городами (индексы 0–4 соответствуют городам 1–5)
distance_matrix = [
    [0, 1, 1, 5, 3],
    [1, 0, 3, 1, 5],
    [1, 3, 0, 11, 1],
    [5, 1, 11, 0, 1],
    [3, 5, 1, 1, 0]
]

# Параметры генетического алгоритма
POPULATION_SIZE = 4
MUTATION_RATE = 0.01
GENERATIONS = 100

# Функция оценки (суммарная длина маршрута)
def fitness(route):
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i+1]]
    total += distance_matrix[route[-1]][route[0]]  # возвращение в начальный город
    return total

# Инициализация популяции случайными маршрутами
def init_population(size, num_cities):
    population = []
    for _ in range(size):
        route = list(range(num_cities))
        random.shuffle(route)
        population.append(route)
    return population

# Турнирный отбор
def select_pair(population, fitnesses):
    def tournament():
        i, j = random.sample(range(len(population)), 2)
        return population[i] if fitnesses[i] < fitnesses[j] else population[j]
    return tournament(), tournament()

# Операция упорядоченного кроссовера (OX)
def crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1]*size

    # Скопировать отрезок из первого родителя
    child[a:b] = parent1[a:b]

    # Заполнить оставшиеся позиции генами из второго родителя
    p2_idx = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[p2_idx] in child:
                p2_idx += 1
            child[i] = parent2[p2_idx]
    return child

# Операция мутации: обмен двух случайных генов
def mutate(route, rate):
    for i in range(len(route)):
        if random.random() < rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]

def genetic_algorithm():
    num_cities = len(distance_matrix)
    population = init_population(POPULATION_SIZE, num_cities)

    for gen in range(GENERATIONS):
        # Оценить приспособленность
        fitnesses = [fitness(ind) for ind in population]

        new_population = []
        while len(new_population) < POPULATION_SIZE:
            # Отбор
            p1, p2 = select_pair(population, fitnesses)
            # Кроссовер
            child = crossover(p1, p2)
            # Мутация
            mutate(child, MUTATION_RATE)
            new_population.append(child)

        population = new_population

        #        if (gen + 1) % 10 == 0:
        #    best_idx = fitnesses.index(min(fitnesses))
        #   print(f"Поколение {gen+1}: Лучший маршрут = {population[best_idx]} с длиной {fitnesses[best_idx]}")

    fitnesses = [fitness(ind) for ind in population]
    best_idx = fitnesses.index(min(fitnesses))
    best_route = population[best_idx]
    best_length = fitnesses[best_idx]
    return best_route, best_length

if __name__ == "__main__":
    route, length = genetic_algorithm()
    route_cities = [city + 1 for city in route]
    print(f"Оптимальный маршрут: {route_cities} с длиной {length}")

