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


def roomDescription_inputs_are_correct(rname, rtype, capacity, ishandicap):
    # Verificar si el nombre de la habitación es válido
    valid_room_names = ['Standard', 'Standard Queen', 'Standard King', 'Double Queen',
                        'Double King', 'Triple King', 'Executive Family', 'Presidential']
    if rname not in valid_room_names:
        return False

    # Verificar si el tipo de habitación es válido para el nombre dado
    valid_room_types = {
        'Standard': ['Basic', 'Premium'],
        'Standard Queen': ['Basic', 'Premium', 'Deluxe'],
        'Standard King': ['Basic', 'Premium', 'Deluxe'],
        'Double Queen': ['Basic', 'Premium', 'Deluxe'],
        'Double King': ['Basic', 'Premium', 'Deluxe', 'Suite'],
        'Triple King': ['Deluxe', 'Suite'],
        'Executive Family': ['Deluxe', 'Suite'],
        'Presidential': ['Suite']
    }
    if rtype not in valid_room_types.get(rname, []):
        return False

    # Verificar la capacidad de la habitación
    valid_capacities = {
        'Standard': [1],
        'Standard Queen': [1, 2],
        'Standard King': [2],
        'Double Queen': [4],
        'Double King': [4, 6],
        'Triple King': [6],
        'Executive Family': [4, 6, 8],
        'Presidential': [4, 6, 8]
    }
    if capacity not in valid_capacities.get(rname, []):
        return False

    # Verificar si es apta para discapacitados
    if not isinstance(ishandicap, bool):
        return False

    return True

