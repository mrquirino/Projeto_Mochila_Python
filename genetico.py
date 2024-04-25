import random

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def read_input_file(filename):
    items = []
    capacity = 0
    with open(filename, 'r') as file:
        capacity = int(file.readline().strip())
        for line in file:
            line = line.strip().split(',')
            if len(line) == 3:
                name = line[0]
                weight = int(line[1])
                value = int(line[2])
                items.append(Item(weight, value))
    return items, capacity


def main():
    # Ler os dados do arquivo
    items, capacity = read_input_file('KNAPDATA40.TXT')

    # Parâmetros do algoritmo genético
    population_size = 50
    crossover_rate = 0.5
    mutation_rate = 0.2
    num_generations = 500

    # Chamada para a função que implementa o algoritmo genético
    solution = genetic_algorithm_knapsack(items, capacity, population_size, crossover_rate, mutation_rate, num_generations)

    # Imprimir a solução encontrada
    print("Itens selecionados:")
    for i, item in enumerate(items):
        if solution[i] == 1:
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")


# Função para implementar o algoritmo genético para o Problema da Mochila
def genetic_algorithm_knapsack(items, capacity, population_size, crossover_rate, mutation_rate, num_generations):
    population = generate_initial_population(len(items), population_size)

    for gen in range(num_generations):
        next_generation = []
        for _ in range(population_size):
            parent1 = tournament_selection(population, items, capacity)
            parent2 = roulette_selection(population, items, capacity)
            offspring1, offspring2 = crossover(parent1, parent2, crossover_rate)  # Dois filhos por cruzamento
            mutate(offspring1, mutation_rate)
            mutate(offspring2, mutation_rate)
            # Comparação entre os filhos e seleção do melhor
            best_offspring = max(offspring1, offspring2, key=lambda x: fitness_function(x, items, capacity))
            next_generation.append(best_offspring)
        population = next_generation

    # Encontrar a melhor solução na última geração
    best_solution = max(population, key=lambda x: fitness_function(x, items, capacity))
    return best_solution

# Função para gerar uma população inicial aleatória
def generate_initial_population(size, population_size):
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(size)]  # 0 ou 1 (selecionado ou não selecionado)
        population.append(individual)
    return population

# Função de fitness para calcular o valor total da mochila
def fitness_function(solution, items, capacity):
    total_value = sum(item.value for item, selected in zip(items, solution) if selected == 1)
    total_weight = sum(item.weight for item, selected in zip(items, solution) if selected == 1)
    # Penalize soluções que excedam a capacidade da mochila
    if total_weight > capacity:
        total_value = 0
    return total_value

# Função para realizar a seleção por torneio
def tournament_selection(population, items, capacity):
    tournament_size = 5  # Tamanho do torneio
    tournament = random.sample(population, tournament_size)
    best_solution = max(tournament, key=lambda x: fitness_function(x, items, capacity))
    return best_solution

# Função para realizar a seleção por roleta
def roulette_selection(population, items, capacity):
    total_fitness = sum(fitness_function(individual, items, capacity) for individual in population)
    random_fitness = random.uniform(0, total_fitness)
    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += fitness_function(individual, items, capacity)
        if cumulative_fitness >= random_fitness:
            return individual

# Função para realizar o cruzamento (crossover)
def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(0, len(parent1))
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        return offspring1, offspring2  # Retorna dois filhos por cruzamento
    else:
        return parent1, parent2  # Sem cruzamento

# Função para realizar a mutação
def mutate(solution, mutation_rate):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            solution[i] = 1 - solution[i]  # Troca entre 0 e 1

if __name__ == "__main__":
    main()
