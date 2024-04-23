import random
import copy

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

    # Parâmetros da Busca Tabu
    tabu_size = 5
    max_iterations = 1000

    # Chamada para a função que implementa a Busca Tabu
    solution = tabu_search_knapsack(items, capacity, tabu_size, max_iterations)

    # Imprimir a solução encontrada
    print("Itens selecionados:")
    for i, item in enumerate(items):
        if solution[i] == 1:
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")

def tabu_search_knapsack(items, capacity, tabu_size, max_iterations):
    current_solution = generate_random_solution(len(items))
    best_solution = copy.deepcopy(current_solution)
    current_cost = cost_function(current_solution, items, capacity)  # Passando a capacidade como parâmetro
    best_cost = current_cost
    tabu_list = []

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current_solution)
        next_solution = None
        next_cost = float('-inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_cost = cost_function(neighbor, items, capacity)  # Passando a capacidade como parâmetro
                if neighbor_cost > next_cost:
                    next_solution = neighbor
                    next_cost = neighbor_cost

        if next_solution is None:
            break

        current_solution = next_solution
        current_cost = next_cost

        if current_cost > best_cost:
            best_solution = copy.deepcopy(current_solution)
            best_cost = current_cost

        tabu_list.append(next_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best_solution

def generate_random_solution(size):
    return [random.randint(0, 1) for _ in range(size)]

def cost_function(solution, items, capacity):  # Adicionando a capacidade como parâmetro
    total_value = 0
    total_weight = 0
    for i, selected in enumerate(solution):
        if selected == 1:
            total_value += items[i].value
            total_weight += items[i].weight
    # Penalize soluções que excedam a capacidade da mochila
    # Implemente o método de penalização que achar mais adequado
    if total_weight > capacity:
        total_value = 0
    return total_value

def generate_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution[:]  # Copia da solução atual
        neighbor[i] = 1 - neighbor[i]  # Troca o valor do item selecionado
        neighbors.append(neighbor)
    return neighbors

if __name__ == "__main__":
    main()
