from django.contrib.auth.admin import UserAdmin

from .models import (Subscription, User,
                     Favorite, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)

from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    list_filter = ('email', 'username')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'count_in_favorites')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline, )

    def count_in_favorites(self, recipe):
        return Favorite.objects.filter(recipe=recipe).count()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
