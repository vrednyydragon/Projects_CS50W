from django.contrib import admin
from .models import UsersLogin, UsersProfile, ItemAttributes, ItemImages, \
	ItemTags, Recepies, RecepiesIngredients, RecepiesInstructions, RelationUserMeal, \
	UsersMealAdditionals, ItemTranslations, RecepiTranslations, RecepiInstructionTranslations, \
	Components, ComponentsTranslations, ItemTranslations, ItemTypesCatalog, ItemsCatalog,\
	Languages, MeasureUnits, MeasureUnitsTranslations, Products, ProductComponents, ProductImages, ProductTags, \
	ProductTranslations, RecepiInstructionTranslations, RecepiTags, RecepiTranslations,\
	Tags, TagsCategory, TagsTranslations, UsersFoodLog

admin.site.register(UsersLogin)
admin.site.register(UsersProfile)
admin.site.register(ItemAttributes)
admin.site.register(ItemImages)
admin.site.register(ItemTags)
admin.site.register(Recepies)
admin.site.register(RecepiesIngredients)
admin.site.register(RecepiesInstructions)
admin.site.register(RelationUserMeal)
admin.site.register(UsersMealAdditionals)
admin.site.register(ItemTranslations)
admin.site.register(RecepiTranslations)
admin.site.register(RecepiInstructionTranslations)
admin.site.register(Components)
admin.site.register(ComponentsTranslations)
admin.site.register(ItemTypesCatalog)
admin.site.register(ItemsCatalog)
admin.site.register(Languages)
admin.site.register(MeasureUnits)
admin.site.register(MeasureUnitsTranslations)
admin.site.register(Products)
admin.site.register(ProductComponents)
admin.site.register(ProductImages)
admin.site.register(ProductTags)
admin.site.register(ProductTranslations)
admin.site.register(RecepiTags)
admin.site.register(Tags)
admin.site.register(TagsCategory)
admin.site.register(TagsTranslations)
admin.site.register(UsersFoodLog)