from .graph import Graph
def risk_order(start, end, g: Graph):
    """
    Returns a list of nodes in the order of their risk level from start to end.
    """
    routes = g.dfs_all_paths(start, end) # Get all possible routes

    # Calculate the total risk of each route
    list_risk = []
    for road, distance in routes:
        total_risk = sum(g.get_node(node).risk_level for node in road) / len(road)
        list_risk.append((road, distance, total_risk))

    if not list_risk:
        print("No se encontraron rutas.")
        return None

    list_risk.sort(key=lambda x: x[2]) # Sort routes by risk level
    return list_risk

def route_according_to_experience(start, end, g: Graph, experience="Principiante"):
    """
    Selects a route from start to end based on experience level ('Principiante', 'Intermedio', 'Experto').
    """
    list_risk = risk_order(start, end, g)

    if not list_risk:
        return None, None, None

    selected_route = None

    if experience == "Experto":
        # Find the route with the highest risk within the range
        candidates = [r for r in list_risk if 3.5 <= r[2] <= 5]
        if candidates:
            selected_route = candidates[-1]
        else:
            experience = "Intermedio" # Move to the next level

    if experience == "Intermedio" and selected_route is None:
        # Find a medium-risk route
        candidates = [r for r in list_risk if 2 <= r[2] < 3.5]
        if candidates:
            selected_route = candidates[len(candidates)//2]  # Choose an intermediate
        else:
            experience = "Principiante" # Move to the next level

    if experience == "Principiante" and selected_route is None:
        # Find a low-risk route
        candidates = [r for r in list_risk if 1 <= r[2] < 2]
        if candidates:
            selected_route = candidates[0]

    if selected_route: # If a route was found
        print(f"Ruta adecuada encontrada.")
        print(f"Ruta: {selected_route[0]}")
        print(f"Distancia: {selected_route[1]} metros")
        print(f"Nivel de riesgo promedio: {selected_route[2]}")
        return selected_route[0], selected_route[2], selected_route[1]  # points, average risk, distance

    else:
        print("No se encontró una ruta adecuada para el nivel de dificultad solicitado.")
        return None, None, None

def safest_route(start, end, g: Graph):
    """
    Returns the safest route from start to end.
    """
    
    list_risk = risk_order(start, end, g) # Get all possible routes
    selected_route = None

    if not list_risk:
        print("No se encontraron rutas.")
        return None, None, None 
    
    selected_route = list_risk[0] # Select the safest route (first in the sorted list)
    return selected_route[0], selected_route[2], selected_route[1] # points, average risk, distance

def route_according_to_distance_and_difficulty (start, end, user_distance, g: Graph, level_risk = 1):
    
    list_distance = risk_order(start, end, g) # Get all possible routes

    if not list_distance: # If no routes were found
        print("No se encontraron rutas.")
        return None, None, None
    
    list_distance.sort(key=lambda x: x[1]) # Sort routes by distance
    list_distance_copy = list_distance.copy()
    selected_route = None
    
    valid_by_distance = [r for r in list_distance if r[1] <= user_distance] # Filter routes by distance
    
    if not valid_by_distance: 
        print("No se encontraron rutas menores o iguales a la distancia solicitada.")
        valid_by_distance = list_distance_copy.copy()
    
    valid_by_risk = [r for r in valid_by_distance if r[2] <= level_risk] # Filter routes by risk level

    # Si hay rutas que cumplen riesgo, elegir la más cercana al límite de distancia permitido
    if valid_by_risk:
        selected_route = min(valid_by_risk, key=lambda r: abs(r[1] - user_distance))
    else:
        # Si no hay rutas con el riesgo aceptado, seleccionar la más cercana al límite de distancia
        selected_route = min(valid_by_distance, key=lambda r: abs(r[1] - user_distance))
        print("No se encontraron rutas con el nivel de riesgo aceptado. Se seleccionó la más cercana en distancia.")

    print(f"Ruta sugerida: {selected_route[0]}")
    print(f"Distancia: {selected_route[1]} metros")
    print(f"Nivel de riesgo promedio: {selected_route[2]}")

    return selected_route[0], selected_route[2], selected_route[1]

def proposed_routes (start, end, user_duration, g: Graph, level_risk = 1, experience="Principiante"):
    """
    Proposes routes based on the duration, user's experience level and risk tolerance.
    """
    list_distance = risk_order(start, end, g)
    if not list_distance:
        print("No se encontraron rutas.")
        return None, None, None
    
    list_distance.sort(key=lambda x: x[1])

    max_distance = user_duration * 1000 / (60 / 15)
    list_distance_copy = list_distance.copy()
    selected_routes = None
    
    valid_by_distance = [r for r in list_distance if r[1] <= max_distance]
    if not valid_by_distance:
        print("No se encontraron rutas menores o iguales a la distancia solicitada.")
        valid_by_distance = list_distance_copy.copy()
    
    valid_by_difficulty = [r for r in valid_by_distance if r[2] <= level_risk]
    if not valid_by_difficulty:
        print("No se encontraron rutas con el nivel de riesgo aceptado. Se seleccionó la más cercana en distancia.")
        valid_by_difficulty = valid_by_distance.copy()
    
    if experience == "Experto":
        # Buscar la ruta con mayor riesgo dentro del rango
        candidates = [r for r in valid_by_difficulty if 3.5 <= r[2] <= 5]
        if candidates:
            selected_routes = candidates.copy()
        else:
            experience = "Intermedio"

    if experience == "Intermedio":
        # Buscar una ruta de riesgo medio
        candidates = [r for r in valid_by_difficulty if 2 <= r[2] < 3.5]
        if candidates:
            selected_routes = candidates.copy()
        else:
            experience = "Principiante"

    if experience == "Principiante":
        # Buscar una ruta de bajo riesgo
        candidates = [r for r in valid_by_difficulty if 1 <= r[2] < 2]
        if candidates:
            selected_routes = candidates.copy()
        else:
            print("No se encontró una ruta adecuada para el nivel de dificultad solicitado.")
            return None, None, None

    return selected_routes    

def min_distances_from (start, g: Graph): #Dijkstra

    list_distance_points = g.dijkstra(start)
    if not list_distance_points:
        print("No se encontraron rutas.")
        return None

    return list_distance_points