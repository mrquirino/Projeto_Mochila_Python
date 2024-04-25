import random
import math

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def main():
    # Ler os dados do arquivo KNAPDATA40.TXT
    items, capacity = read_instance("KNAPDATA40.TXT")

    # Parâmetros do Simulated Annealing
    initial_temperature = 1000
    cooling_rate = 0.95
    num_iterations = 1000

    # Chamada para a função que implementa o Simulated Annealing
    solution = simulated_annealing_knapsack(items, capacity, initial_temperature, cooling_rate, num_iterations)

    # Imprimir a solução encontrada
    print("Itens selecionados:")
    total_weight = 0
    total_value = 0
    for i, item in enumerate(items):
        if solution[i] == 1:
            print(f"Item {i+1}: Peso = {item.weight}, Valor = {item.value}")
            total_weight += item.weight
            total_value += item.value
    print(f"Peso total: {total_weight}")
    print(f"Valor total: {total_value}")

def simulated_annealing_knapsack(items, capacity, initial_temperature, cooling_rate, num_iterations):
    current_solution = generate_random_solution(len(items))
    best_solution = current_solution[:]
    current_cost = cost_function(current_solution, items, capacity)
    best_cost = current_cost
    temperature = initial_temperature

    for _ in range(num_iterations):
        new_solution = generate_neighbor(current_solution)
        new_cost = cost_function(new_solution, items, capacity)

        if new_cost > current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution[:]
            current_cost = new_cost

        if current_cost > best_cost:
            best_solution = current_solution[:]
            best_cost = current_cost

        temperature *= cooling_rate

    return best_solution

def generate_random_solution(size):
    return [random.randint(0, 1) for _ in range(size)]

def cost_function(solution, items, capacity):
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

def generate_neighbor(solution):
    # Escolhe um índice aleatório para trocar o item selecionado por não selecionado, ou vice-versa
    neighbor = solution[:]
    index = random.randint(0, len(solution) - 1)
    neighbor[index] = 1 - neighbor[index]  # Troca entre 0 e 1
    return neighbor

def read_instance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Capacidade da mochila é o primeiro valor
    capacity = int(lines[0].strip())

    # Número total de itens é o segundo valor
    num_items = int(lines[1].strip())

    items = []
    for line in lines[2:]:
        parts = line.strip().split(',')
        name = parts[0]
        weight = int(parts[1])
        value = int(parts[2])
        items.append(Item(weight, value))

    return items, capacity


if __name__ == "__main__":
    main()
