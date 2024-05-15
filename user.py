import json
import os


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.name = username
        self.keys = {
            "Имя": None,
            "Пинок": False,
            "Положительно": False,
            "Да, стоит": False,
            "Нет, не стоит": False,
            "Битый телик": False,
            "Телик": False,
            "Браузер": False,
            "Смайл": False,
            "Бумага": False,
            "Флешка и ноут": False
        }
        self.relationship_with_ann = {
            "Безмолвие": 0,
            "Цикл 1": 0
        }
        self.fragments = {
            "Карманная сверхновая": 0
        }
        self.inventory = {
            "Плюшевый кролик": False,
            "Деревянная бита": False,
            "Солнцезащитные очки": False,
            "Флешка": 0,
            "Бумаги": 0
        }
        self.current_stage = 1
        self.save_counter = 0

    def update_keys(self, key, value):
        if key in self.keys:
            self.keys[key] = value

    def update_relationship_with_ann(self, relationship, value):
        if relationship in self.relationship_with_ann:
            self.relationship_with_ann[relationship] = value

    def update_fragments(self, fragment, value):
        if fragment in self.fragments:
            self.fragments[fragment] = value

    def update_inventory(self, item, value):
        if item in self.inventory:
            self.inventory[item] = value

    def update_current_stage(self, stage):
        self.current_stage = stage

    def __str__(self):
        out_txt = ''
        for key, value in self.inventory.items():
            if value:
                out_txt += f'\n*{key}* {': ' + str(value) if type(value) is int else ''}'
        if self.fragments["Карманная сверхновая"]:
            out_txt += "\nФрагменты:\n*Карманная сверхновая:* " + str(self.fragments["Карманная сверхновая"])
        if out_txt != '':
            return 'Инвентарь: \n' + out_txt
        else:
            return "_Инвентарь пуст_"

    def save_user(self):
        data = {
            "user_id": self.user_id,
            "name": self.name,
            "keys": self.keys,
            "relationship_with_ann": self.relationship_with_ann,
            "fragments": self.fragments,
            "inventory": self.inventory,
            "current_stage": self.current_stage
        }
        with open(f"users/{self.user_id}.json", "w") as file:
            json.dump(data, file)

    def delete_user(self):
        os.remove(f"users/{self.user_id}.json")


def load_user(user_id):
    with open(f"users/{user_id}.json", "r") as file:
        data = json.load(file)
    user = User(data["user_id"], data["name"])
    user.keys = data["keys"]
    user.relationship_with_ann = data["relationship_with_ann"]
    user.fragments = data["fragments"]
    user.inventory = data["inventory"]
    user.current_stage = data["current_stage"]
    return user
