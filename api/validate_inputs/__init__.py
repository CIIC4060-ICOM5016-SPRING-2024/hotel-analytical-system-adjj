def employee_inputs_are_correct(position, salary):
    # Asegurarse de que la posición sea válida
    if position not in ['Regular', 'Supervisor', 'Administrator']:
        print(f"Error: La posición {position} no es válida.")
        return False

    # Asegurarse de que el salario cumpla con las reglas según la posición
    salary_rules = {
        'Regular': (18000, 49999),
        'Supervisor': (50000, 79000),
        'Administrator': (80000, 120000)
    }

    min_salary, max_salary = salary_rules[position]
    if not (min_salary <= salary <= max_salary):
        print(f"Error: El salario {salary} no cumple con las reglas para la posición {position}.")
        return False

    return True