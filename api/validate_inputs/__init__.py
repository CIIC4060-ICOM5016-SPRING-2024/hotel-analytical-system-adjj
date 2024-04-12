def employee_inputs_are_correct(position, salary):
    message = "The entries are correct"
    # Asegurarse de que la posición sea válida
    if position not in ['Regular', 'Supervisor', 'Administrator']:
        #print(f"Error: La posición {position} no es válida.")
        message = f"Position {position} is invalid. It should be 'Regular', 'Supervisor' or 'Administrator'."
        return False, message

    # Asegurarse de que el salario cumpla con las reglas según la posición
    salary_rules = {
        'Regular': (18000, 49999),
        'Supervisor': (50000, 79000),
        'Administrator': (80000, 120000)
    }

    min_salary, max_salary = salary_rules[position]
    if not (min_salary <= salary <= max_salary):
        #print(f"Error: El salario {salary} no cumple con las reglas para la posición {position}.")
        message = f"Error: Salary {salary} does not comply with the rules for position {position}. The salaries are as follows: {salary_rules}"
        return False, message

    return True, message


def post_room_description_validation(rname, rtype, capacity):
    # Dictionary to hold the valid capacities and types for each room name
    valid_descriptions = {
        'Standard': {'capacities': [1], 'types': ['Basic', 'Premium']},
        'Standard Queen': {'capacities': [1, 2], 'types': ['Basic', 'Premium', 'Deluxe']},
        'Standard King': {'capacities': [2], 'types': ['Basic', 'Premium', 'Deluxe']},
        'Double Queen': {'capacities': [4], 'types': ['Basic', 'Premium', 'Deluxe']},
        'Double King': {'capacities': [4, 6], 'types': ['Basic', 'Premium', 'Deluxe', 'Suite']},
        'Triple King': {'capacities': [6], 'types': ['Deluxe', 'Suite']},
        'Executive Family': {'capacities': [4, 6, 8], 'types': ['Deluxe', 'Suite']},
        'Presidential': {'capacities': [4, 6, 8], 'types': ['Suite']}
    }

    # Check if the room name is valid
    if rname not in valid_descriptions:
        return False, valid_descriptions

    # Check if the capacity and type are valid for the given room name
    if capacity in valid_descriptions[rname]['capacities'] and rtype in valid_descriptions[rname]['types']:
        return True, valid_descriptions
    else:
        return False, valid_descriptions


