import json
import os
from pathlib import Path

class IDManager:
    def __init__(self, file_path='database/ids.json'):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_data()
        
    def _load_data(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "next_user_id": 0,
                "init_point_id": 100,
                "users": {}
            }
    
    def _save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def create_new_user(self):
        current_id = self.data["next_user_id"]
        self.data["users"][str(current_id)] = {
            "next_route_id": 0,
            "next_point_id": self.data["init_point_id"]
        }
        self.data["next_user_id"] += 1
        self._save_data()
        return current_id

    def get_new_route_id(self, user_id):
        user_str = str(user_id)
        if user_str not in self.data["users"]:
            raise ValueError(f"El usuario {user_id} no existe")
        
        new_id = self.data["users"][user_str]["next_route_id"]
        self.data["users"][user_str]["next_route_id"] += 1
        self._save_data()
        return new_id

    def get_new_point_id(self, user_id):
        user_str = str(user_id)
        if user_str not in self.data["users"]:
            raise ValueError(f"El usuario {user_id} no existe")
        
        new_id = self.data["users"][user_str]["next_point_id"]
        self.data["users"][user_str]["next_point_id"] += 1
        self._save_data()
        return new_id

# Uso ejemplo
if __name__ == "__main__":
    id_manager = IDManager()
    
    # Crear nuevo usuario
    nuevo_usuario = id_manager.create_new_user()
    print(f"Nuevo usuario ID: {nuevo_usuario}")
    
    # Obtener IDs para el usuario
    print(f"Nueva ruta ID: {id_manager.get_new_route_id(nuevo_usuario)}")
    print(f"Nuevo punto ID: {id_manager.get_new_point_id(nuevo_usuario)}")