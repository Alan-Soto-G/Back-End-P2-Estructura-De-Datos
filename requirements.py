import graph
import json
import os

def route_according_to_difficulty (start, end, g:graph.Graph):
    """
    This function creates a graph of routes and their difficulties, then finds the shortest path
    from the start to the end node based on difficulty.
    """
    routes = g.dfs_all_paths(start, end)


def main (self, user_id, start, end):
    
    PATH = "./database/users_routes.json"

    if not os.path.exists(PATH):
        print("Data file not found.")
        return
    
    with open(PATH, "r") as file:
        map = json.load(file)

    user_data = map["users"].get(str(user_id))

    if user_data:
        g = graph.Graph()
        points = user_data["points"]
        edges = user_data["edges"]
        
        for point in points:
            g.add_node(point["id"], point["name"], point["description"], point["risk_level"])
            
        for edge in edges:
            g.add_edge(edge["from"], edge["to"], edge["distance_meters"], edge["directed"])
    else:
        print(f"Usuario con ID {user_id} no encontrado.")

    route_according_to_difficulty(start, end, g)
