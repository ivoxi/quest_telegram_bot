class Stage:
    def __init__(self, number, description, choices=None, updates=None, is_ending=False, ending_name=None, image=None):
        self.number = number
        self.description = description
        self.choices = choices or None
        self.updates = updates or None
        self.is_ending = is_ending
        self.ending_name = ending_name or None
        self.image = image or None

    def apply_choice(self, user, choice_key):
        choice = self.choices[choice_key - 1]
        if choice:
            if self.updates is not None:
                for attribute, value in self.updates.items():
                    if attribute in user.keys:
                        user.update_keys(attribute, value)
                    elif attribute in user.relationship_with_ann:
                        user.update_relationship_with_ann(attribute, value)
                    elif attribute in user.inventory:
                        user.update_inventory(attribute, value)
                    elif attribute in user.fragments:
                        user.update_fragments(attribute, value)
            if 'update' in choice:
                updates = choice['update']
                for attribute, value in updates.items():
                    if attribute in user.keys:
                        user.update_keys(attribute, value)
                    elif attribute in user.relationship_with_ann:
                        user.update_relationship_with_ann(attribute, value)
                    elif attribute in user.inventory:
                        user.update_inventory(attribute, value)
                    elif attribute in user.fragments:
                        user.update_fragments(attribute, value)

            if 'next_stage' in choice:
                user.update_current_stage(choice['next_stage'])

    def get_description(self):
        return self.description

    def get_choices(self, user):
        user_choices = []
        for choice in self.choices:
            result = True
            if 'conditions' in choice:
                if 'logical_operator' in choice:
                    logical_operator = choice['logical_operator']
                else:
                    logical_operator = "AND"
                local_results = []
                for condition in choice['conditions']:
                    part, key, symbol, value = condition
                    current_value = getattr(user, part).get(key, None)
                    if symbol == "=":
                        result = (current_value == value)
                    elif symbol == "<":
                        result = (current_value < value)
                    elif symbol == ">":
                        result = (current_value > value)
                    elif symbol == "exist":
                        result = (current_value != value)
                    else:
                        raise ValueError("Неверный условный символ")

                    local_results.append(result)

                if logical_operator == "AND":
                    result = all(local_results)
                elif logical_operator == "OR":
                    result = any(local_results)
                else:
                    raise ValueError("Неверный логический оператор")
            if result:
                user_choices.append(choice)
        self.choices = user_choices
        return self.choices
