import pytest
from recipes import Ingredient, Recipe, ShoppingList


def test_ingredient_initialization():
    ingredient = Ingredient("Соль", 1000, "г")
    assert ingredient.name == "Соль"
    assert ingredient.quantity == 1000.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Соль", 1000, "г")
    assert str(ingredient) == "Соль: 1000.0 г"


def test_ingredient_same():
    ing_1 = Ingredient("Соль", 1000, "г")
    ing_2 = Ingredient("Соль", 777, "г")
    assert ing_1 == ing_2


@pytest.mark.parametrize("first, second, expected",
    [(Ingredient("Мука", 500, "г"), Ingredient("Мука", 1000, "г"), True),
     (Ingredient("Мука", 500, "г"), Ingredient("Сахар", 500, "г"), False),
     (Ingredient("Мука", 500, "г"), Ingredient("Мука", 500, "кг"), False),])
def test_ingredient_eq(first, second, expected):
    assert (first == second) == expected


@pytest.mark.parametrize("quantity", [0, -1, -100])
def test_ingredient_invalid_quantity(quantity):
    with pytest.raises(ValueError):
        Ingredient("Соль", quantity, "г")


def test_recipe_initialization():
    recipe = Recipe("Сыр косичка")
    assert recipe.title == "Сыр косичка"
    assert recipe.ingredients == []


def test_recipe_new_ingredient():
    recipe = Recipe("Пицца")
    ingredient = Ingredient("Мука", 500, "г")
    recipe.add_ingredient(ingredient)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[0].unit == "г"


def test_recipe_add_same_ingredient():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0


def test_recipe_scale_does_not_change_original_recipe():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled_recipe = recipe.scale(2)
    assert recipe.ingredients[0].quantity == 500.0
    assert scaled_recipe.ingredients[0].quantity == 1000.0


def test_recipe_scale_new_recipe():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled_recipe = recipe.scale(2)
    assert isinstance(scaled_recipe, Recipe)
    assert scaled_recipe is not recipe


def test_recipe_scale():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Соль", 10, "г"))
    scaled_recipe = recipe.scale(2)
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert scaled_recipe.ingredients[1].quantity == 20.0


def test_recipe_scale_error():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    recipe.add_ingredient(Ingredient("Соль", 10, "г"))
    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    recipe = Recipe("Макароны с фаршем")
    recipe.add_ingredient(Ingredient("Фарш", 500, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Фарш"
    assert result[0].quantity == 1000.0
    assert result[0].unit == "г"


def test_shopping_list_add_error():
    recipe = Recipe("Макароны с фаршем")
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    pasta = Recipe("Макароны с фаршем")
    pasta.add_ingredient(Ingredient("Фарш", 500, "г"))
    pancakes = Recipe("Блины")
    pancakes.add_ingredient(Ingredient("Молоко", 200, "мл"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pasta, 1)
    shopping_list.add_recipe(pancakes, 1)
    shopping_list.remove_recipe("Макароны с фаршем")
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Молоко"


def test_shopping_list_remove_recipe_no_error():
    recipe = Recipe("Макароны с фаршем")
    recipe.add_ingredient(Ingredient("Фарш", 500, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    shopping_list.remove_recipe("Суп")
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Фарш"


def test_shopping_list_get_list_same():
    pelmeni = Recipe("Пельмени")
    pelmeni.add_ingredient(Ingredient("Мука", 500, "г"))
    cake = Recipe("Торт")
    cake.add_ingredient(Ingredient("Мука", 500, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pelmeni, 1)
    shopping_list.add_recipe(cake, 2)
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 1500.0


def test_shopping_list_get_list_sorted_by_name():
    recipe = Recipe("Еда")
    recipe.add_ingredient(Ingredient("Банан", 2, "шт"))
    recipe.add_ingredient(Ingredient("Апельсин", 3, "шт"))
    recipe.add_ingredient(Ingredient("Яблоко", 5, "шт"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    result = shopping_list.get_list()
    names = [ingredient.name for ingredient in result]
    assert names == ["Апельсин", "Банан", "Яблоко"]


def test_shopping_list_add_lists():
    breakfast = Recipe("Завтрак")
    breakfast.add_ingredient(Ingredient("Яйцо", 2, "шт"))
    salad = Recipe("Салат")
    salad.add_ingredient(Ingredient("Огурец", 1, "шт"))
    first_list = ShoppingList()
    first_list.add_recipe(breakfast, 1)
    second_list = ShoppingList()
    second_list.add_recipe(salad, 1)
    new_list = first_list + second_list
    result = new_list.get_list()
    names = [ingredient.name for ingredient in result]
    assert names == ["Огурец", "Яйцо"]


def test_shopping_list_add_not_change():
    breakfast = Recipe("Завтрак")
    breakfast.add_ingredient(Ingredient("Яйцо", 2, "шт"))
    salad = Recipe("Салат")
    salad.add_ingredient(Ingredient("Огурец", 1, "шт"))
    first_list = ShoppingList()
    first_list.add_recipe(breakfast, 1)
    second_list = ShoppingList()
    second_list.add_recipe(salad, 1)
    new_list = first_list + second_list
    assert len(first_list.get_list()) == 1
    assert len(second_list.get_list()) == 1
    assert len(new_list.get_list()) == 2