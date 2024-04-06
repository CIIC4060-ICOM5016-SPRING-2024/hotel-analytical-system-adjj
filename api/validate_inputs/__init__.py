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


# def post_room_description_validation(rname, rtype, capacity):
#     # Define the valid types and capacities for each room name
#     room_specs = {
#         'Standard': {
#             'types': ['Basic', 'Premium'],
#             'capacities': [1]
#         },
#         'Standard Queen': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [1, 2]
#         },
#         'Standard King': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [2]
#         },
#         'Double Queen': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [4]
#         },
#         'Double King': {
#             'types': ['Basic', 'Premium', 'Deluxe', 'Suite'],
#             'capacities': [4, 6]
#         },
#         'Triple King': {
#             'types': ['Deluxe', 'Suite'],
#             'capacities': [6]
#         },
#         'Executive Family': {
#             'types': ['Deluxe', 'Suite'],
#             'capacities': [4, 6, 8]
#         },
#         'Presidential': {
#             'types': ['Suite'],
#             'capacities': [4, 6, 8]
#         }
#     }
#
#     # Validate the room name
#     if rname not in room_specs:
#         return "Invalid room name."
#
#
#     # Validate the capacity and type for the given room name
#     valid_types = room_specs[rname]['types']
#     valid_capacities = room_specs[rname]['capacities']
#
#     if rtype not in valid_types:
#         return "Invalid room type for the given room name."
#
#     if capacity not in valid_capacities:
#         return "Invalid capacity for the given room name."
#
#     return "Valid room description."

#
#
# def post_room_description_validation(rname, rtype, capacity):
#     # Define the valid types and capacities for each room name
#     room_specs = {
#         'Standard': {
#             'types': ['Basic', 'Premium'],
#             'capacities': [1]
#         },
#         'Standard Queen': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [1, 2]
#         },
#         'Standard King': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [2]
#         },
#         'Double Queen': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [4]
#         },
#         'Double King': {
#             'types': ['Basic', 'Premium', 'Deluxe', 'Suite'],
#             'capacities': [4, 6]
#         },
#         'Triple King': {
#             'types': ['Deluxe', 'Suite'],
#             'capacities': [6]
#         },
#         'Executive Family': {
#             'types': ['Deluxe', 'Suite'],
#             'capacities': [4, 6, 8]
#         },
#         'Presidential': {
#             'types': ['Suite'],
#             'capacities': [4, 6, 8]
#         }
#     }
#
#     # Validate the room name
#     if rname not in room_specs:
#         return "Invalid room name."
#
#     # Validate the capacity and type for the given room name
#     valid_types = room_specs[rname]['types']
#     valid_capacities = room_specs[rname]['capacities']
#
#     if rtype not in valid_types:
#         return "Invalid room type for the given room name."
#
#     if capacity not in valid_capacities:
#         return "Invalid capacity for the given room name."
#
#     return "Valid room description."
#
#
# def post_room_description_validation(rname, rtype, capacity):
#     # Convert capacity to integer if it's not already
#     try:
#         capacity = int(capacity)
#     except ValueError:
#         return "Invalid capacity format. Capacity must be an integer."
#
#     # Define the valid types and capacities for each room name
#     room_specs = {
#         'Standard': {
#             'types': ['Basic', 'Premium'],
#             'capacities': [1]
#         },
#         'Standard Queen': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [1, 2]
#         },
#         'Standard King': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [2]
#         },
#         'Double Queen': {
#             'types': ['Basic', 'Premium', 'Deluxe'],
#             'capacities': [4]
#         },
#         'Double King': {
#             'types': ['Basic', 'Premium', 'Deluxe', 'Suite'],
#             'capacities': [4, 6]
#         },
#         'Triple King': {
#             'types': ['Deluxe', 'Suite'],
#             'capacities': [6]
#         },
#         'Executive Family': {
#             'types': ['Deluxe', 'Suite'],
#             'capacities': [4, 6, 8]
#         },
#         'Presidential': {
#             'types': ['Suite'],
#             'capacities': [4, 6, 8]  # Corrected capacities
#         }
#     }
#
#     # Validate the room name
#     if rname not in room_specs:
#         return "Invalid room name."
#
#     # Validate the capacity and type for the given room name
#     valid_types = room_specs[rname]['types']
#     valid_capacities = room_specs[rname]['capacities']
#
#     if rtype not in valid_types:
#         return "Invalid room type for the given room name."
#
#     if capacity not in valid_capacities:
#         return f"Invalid capacity for the given room name. Valid capacities for {rname} are: {valid_capacities}."
#
#     return "Valid room description."


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
        return False

    # Check if the capacity and type are valid for the given room name
    if capacity in valid_descriptions[rname]['capacities'] and rtype in valid_descriptions[rname]['types']:
        return True
    else:
        return False


