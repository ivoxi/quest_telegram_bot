import json


class Endings:
    def __init__(self, user_id):
        self.user_id = user_id
        self.endings = {
            "Ты не одинока": False,
            "Закрой глаза": False,
            "Доигрался": False,
            "Домашний любимец": False,
            "Чужое тело": False,
            "Вперёд!": False,
        }

    def update_endings(self, key, value=True):
        if key in self.endings:
            self.endings[key] = value

    def __str__(self):
        if True in self.endings.values():
            return "Ваши концовки:\n" + "\n".join(f"*{key}*" for key, value in self.endings.items() if value)
        else:
            return "Список концовок пока пуст"

    def save_endings(self):
        with open(f"endings/{self.user_id}.json", "w") as file:
            json.dump(self.endings, file)


def load_endings(user_id):
    try:
        with open(f"endings/{user_id}.json", "r") as file:
            data = json.load(file)
        endings = Endings(user_id)
        endings.endings = data
        return endings
    except FileNotFoundError:
        endings = Endings(user_id)
        endings.save_endings()
        return endings
