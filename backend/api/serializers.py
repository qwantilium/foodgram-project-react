from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField, ValidationError)

from recipes.models import (User, Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Subscription, Tag)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return not user.is_anonymous and Subscription.objects.filter(
            user=user,
            author=author.id
        ).exists()


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        read_only=True,
        many=True
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=recipe).exists()

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise ValidationError('В рецепте не заполнены ингредиенты!')
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError('В рецепте не заполнены теги!')
        return tags

    def validate_image(self, image):
        if not image:
            raise ValidationError('Добавьте картинку рецепта!')
        return image

    def validate_name(self, name):
        if not name:
            raise ValidationError('Не заполнено название рецепта!')
        if self.context.get('request').method == 'POST':
            current_user = self.context.get('request').user
            if Recipe.objects.filter(author=current_user, name=name).exists():
                raise ValidationError(
                    'Рецепт с таким названием у вас уже есть!'
                )
        return name

    def validate_text(self, text):
        if not text:
            raise ValidationError('Не заполнено описание рецепта!')
        return text

    def validate_cooking_time(self, cooking_time):
        if not cooking_time:
            raise ValidationError('Не заполнено время приготовления рецепта!')
        return cooking_time

    def create_recipe_ingredients(self, ingredients, recipe):
        for i in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=i.get('id'),
                amount=i.get('amount'),
            )

    def create(self, validated_data):
        ingredients = self.validate_ingredients(
            self.initial_data.get('ingredients')
        )
        tags = self.validate_tags(
            self.initial_data.get('tags')
        )
        recipe = Recipe.objects.create(**validated_data)
        self.create_recipe_ingredients(
            ingredients,
            recipe
        )
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        recipe = super().update(recipe, validated_data)
        if ingredients:
            recipe.ingredients.clear()
            self.create_recipe_ingredients(ingredients, recipe)
        if tags:
            recipe.tags.set(tags)
        return recipe


class RecipeMinifiedSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(CustomUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, author):
        return author.recipes.count()

    def get_recipes(self, author):
        recipes = author.recipes.all()
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit'
        )
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeMinifiedSerializer(recipes, many=True).data
