import graph
def risk_order(start, end, g: graph.Graph):
    """
    Returns a list of nodes in the order of their risk level from start to end.
    """
    # Obtener todas las rutas posibles
    routes = g.dfs_all_paths(start, end)

    # Calcular el riesgo total de cada ruta
    list_risk = []
    for road, distance in routes:
        total_risk = sum(g.get_node(node).risk_level for node in road) / len(road)
        list_risk.append((road, distance, total_risk))

    if not list_risk:
        print("No se encontraron rutas.")
        return None

    # Ordenar rutas por nivel de riesgo
    list_risk.sort(key=lambda x: x[2])

    return list_risk

def route_according_to_experience(start, end, g: graph.Graph, experience="Principiante"):
    """
    Selects a route from start to end based on experience level ('Principiante', 'Intermedio', 'Experto').
    """

    list_risk = risk_order(start, end, g)

    if not list_risk:
        return None, None, None

    selected_route = None

    if experience == "Experto":
        # Buscar la ruta con mayor riesgo dentro del rango
        candidates = [r for r in list_risk if 3.5 <= r[2] <= 5]
        if candidates:
            selected_route = candidates[-1]
        else:
            experience = "Intermedio"  # Pasar al siguiente nivel

    if experience == "Intermedio" and selected_route is None:
        # Buscar una ruta de riesgo medio
        candidates = [r for r in list_risk if 2 <= r[2] < 3.5]
        if candidates:
            selected_route = candidates[len(candidates)//2]  # Elegir una intermedia
        else:
            experience = "Principiante"

    if experience == "Principiante" and selected_route is None:
        # Buscar una ruta de bajo riesgo
        candidates = [r for r in list_risk if 1 <= r[2] < 2]
        if candidates:
            selected_route = candidates[0]
    
    if selected_route:
        print(f"Ruta adecuada encontrada.")
        print(f"Ruta: {selected_route[0]}")
        print(f"Distancia: {selected_route[1]} metros")
        print(f"Nivel de riesgo promedio: {selected_route[2]}")
        return selected_route[0], selected_route[2], selected_route[1]  # puntos, riesgo promedio, distancia

    else:
        print("No se encontró una ruta adecuada para el nivel de dificultad solicitado.")
        return None, None, None

def safest_route(start, end, g: graph.Graph):
    """
    Returns the safest route from start to end.
    """
    
    list_risk = risk_order(start, end, g)
    selected_route = None

    if not list_risk:
        print("No se encontraron rutas.")
        return None, None, None 
    
    selected_route = list_risk[0]
    return selected_route[0], selected_route[2], selected_route[1]

def route_according_to_distance_and_difficulty (start, end, user_distance, g: graph.Graph, level_risk = 1):
    
    list_distance = risk_order(start, end, g)

    if not list_distance:
        print("No se encontraron rutas.")
        return None, None, None

    list_distance.sort(key=lambda x: x[1])
    list_distance_copy = list_distance.copy()
    selected_route = None
    
    valid_by_distance = [r for r in list_distance if r[1] <= user_distance]
    
    if not valid_by_distance:
        print("No se encontraron rutas menores o iguales a la distancia solicitada.")
        valid_by_distance = list_distance_copy.copy()
    
    # Filtrar por riesgo aceptable
    valid_by_risk = [r for r in valid_by_distance if r[2] <= level_risk]

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

def proposed_routes (start, end, user_duration, g: graph.Graph, level_risk = 1, experience="Principiante"):
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

def min_distances_from (start, g:graph.Graph): #Dijkstra

    list_distance_points = g.dijkstra(start)
    if not list_distance_points:
        print("No se encontraron rutas.")
        return None

    return list_distance_points

def main (self, user_id, start, end, popularity=0, experience="Principiante", level_risk=1, user_distance=0):
    import json; import os; import random;
    
    PATH = "./database/users_routes.json"

    if not os.path.exists(PATH):
        print("Data file not found.")
        return
    
    with open(PATH, "r") as file:
        map_data = json.load(file)

    user_data = map_data["users"].get(str(user_id))

    if user_data:
        g = graph.Graph()
        points = user_data["points"]
        edges = user_data["edges"]
        
        for point in points:
            g.add_node(point["id"], point["name"], point["description"], point["risk_level"])
            
        for edge in edges:
            g.add_edge(edge["from"], edge["to"], edge["distance_meters"], edge["directed"])
    
        route_nodes, difficulty, total_distance = route_according_to_experience(start, end, g, experience)
        route_nodes2, difficulty2, total_distance2 = safest_route(start, end, g)
        route_nodes3, difficulty3, total_distance3 = route_according_to_distance_and_difficulty(start, end, user_distance, g, level_risk)
        route_nodes4, difficulty4, total_distance4 = proposed_routes(start, end, user_distance, g, level_risk, experience)


        if route_nodes is not None:
            # Crear entrada de la nueva ruta
            new_route1 = {
                "route_id": str(len(user_data.get("routes", []))),  # ID basado en el número de rutas actuales
                "name": "Ruta generada",
                "popularity": random.randint(1, 5),  # Valor inicial
                "difficulty": difficulty,
                "points": route_nodes,
                "distance_meters": total_distance,
                "duration_minutes": (total_distance / 1000) * (60 / 15)  # 15 km/h
            }
            new_route2 = {
                "route_id": str(len(user_data.get("routes", [])) + 1),  # ID basado en el número de rutas actuales
                "name": "Ruta generada",
                "popularity": random.randint(1, 5),  # Valor inicial
                "difficulty": difficulty2,
                "points": route_nodes2,
                "distance_meters": total_distance2,
                "duration_minutes": (total_distance2 / 1000) * (60 / 15)  # 15 km/h
            }             
            # Añadir al JSON
            if "routes" not in user_data:
                user_data["routes"] = []
            user_data["routes"].append(new_route1)
            user_data["routes"].append(new_route2)

            # Guardar cambios en el archivo
            with open(PATH, "w") as file:
                json.dump(map_data, file, indent=4)

            print("Ruta guardada exitosamente.")
        else:
            print("No se pudo guardar ninguna ruta.")
    
    else:
        print(f"Usuario con ID {user_id} no encontrado.")