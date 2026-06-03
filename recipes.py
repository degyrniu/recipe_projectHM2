class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(quantity)


    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"


    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"


    def __eq__(self, other):
        if isinstance(other, Ingredient) and self.name == other.name and self.unit == other.unit:
            return True
        return False



class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients


    def add_ingredient(self, ingredient: Ingredient):
        flag = False
        for el in self.ingredients:
            if el == ingredient:
                el.quantity += ingredient.quantity
                flag = True
                break
        if not flag:
            self.ingredients.append(ingredient)


    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0


    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError
        new_recipe = Recipe(self.title)
        for el in self.ingredients:
            new_ingredient = Ingredient(el.name, el.quantity * ratio, el.unit)
            new_recipe.add_ingredient(new_ingredient)
        return new_recipe


    def __len__(self):
        return len(self.ingredients)


    def __str__(self):
        st = f"{self.title}:\n"
        for el in self.ingredients:
            st += f"{el}\n"
        return st.strip()


