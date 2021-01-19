from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class UsersLogin(models.Model):
    id_users = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=10)
    date_of_creation = models.DateTimeField()
    login_flag = models.BooleanField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'users_login'


class UsersProfile(models.Model):
    id_profile = models.OneToOneField(UsersLogin, models.DO_NOTHING, db_column='id_profile', primary_key=True)
    date_of_birth = models.DateField()
    gender = models.TextField()
    user_height = models.DecimalField(max_digits=5, decimal_places=2) #(max_digits=65535, decimal_places=65535)
    user_weight = models.DecimalField(max_digits=5, decimal_places=2)
    type_of_food = models.TextField()
    activity_level = models.DecimalField(max_digits=3, decimal_places=2)
    profile_img = models.TextField()

    class Meta:
        managed = False
        db_table = 'users_profile'


class ItemAttributes(models.Model):
    item_id = models.IntegerField(blank=True, null=True)
    attribute_name = models.TextField(blank=True, null=True)
    attribute_sizing = models.TextField(blank=True, null=True)
    attribute_val = models.TextField(blank=True, null=True)
    item_uid = models.ForeignKey('Recepies', models.DO_NOTHING, db_column='item_uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_attributes'


class ItemImages(models.Model):
    item_id = models.IntegerField(blank=True, null=True)
    image_proirity = models.IntegerField(blank=True, null=True)
    image_name = models.TextField(blank=True, null=True)
    item_uid = models.ForeignKey('Recepies', models.DO_NOTHING, db_column='item_uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_images'


class ItemTags(models.Model):
    item_id = models.IntegerField(blank=True, null=True)
    tag_name = models.TextField(blank=True, null=True)
    item_uid = models.ForeignKey('Recepies', models.DO_NOTHING, db_column='item_uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_tags'


class Recepies(models.Model):
    recepi_uid = models.UUIDField(primary_key=True)
    recepi_id = models.IntegerField(blank=True, null=True)
    recepi_name = models.TextField(blank=True, null=True)
    recepi_src_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepies'


# class RecepiesIngredients(models.Model):
#     recepi_id = models.IntegerField(blank=True, null=True)
#     product_id = models.IntegerField(blank=True, null=True)
#     ingredient_desc = models.TextField(blank=True, null=True)
#     ingredient_amount = models.TextField(blank=True, null=True)
#     recepi_uid = models.ForeignKey(Recepies, models.DO_NOTHING, db_column='recepi_uid', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'recepies_ingredients'
class Products(models.Model):
    product_uid = models.UUIDField(primary_key=True)
    product_id = models.IntegerField()
    product_name = models.TextField(blank=True, null=True)
    product_src_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

class MeasureUnits(models.Model):
    measure_unit_uid = models.UUIDField(primary_key=True)
    measure_unit_id = models.IntegerField()
    measure_unit_name = models.TextField(blank=True, null=True)
    measure_unit_src_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measure_units'

class RecepiesIngredients(models.Model):
    recepi_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    ingredient_desc = models.TextField(blank=True, null=True)
    ingredient_amount = models.TextField(blank=True, null=True)
    recepi_uid = models.ForeignKey(Recepies, models.DO_NOTHING, db_column='recepi_uid', blank=True, null=True)
    product_uid = models.ForeignKey(Products, models.DO_NOTHING, db_column='product_uid', blank=True, null=True)
    measure_unit_uid = models.ForeignKey(MeasureUnits, models.DO_NOTHING, db_column='measure_unit_uid', blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    measure_unit_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepies_ingredients'

# class RecepiesInstructions(models.Model):
#     recepi_id = models.IntegerField(blank=True, null=True)
#     step_number = models.IntegerField(blank=True, null=True)
#     step_description = models.TextField(blank=True, null=True)
#     recepi_uid = models.ForeignKey(Recepies, models.DO_NOTHING, db_column='recepi_uid', blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'recepies_instructions'

class RecepiesInstructions(models.Model):
    recepi_id = models.IntegerField(blank=True, null=True)
    step_number = models.IntegerField(blank=True, null=True)
    step_description = models.TextField(blank=True, null=True)
    recepi_uid = models.ForeignKey(Recepies, models.DO_NOTHING, db_column='recepi_uid', blank=True, null=True)
    instruction_uid = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'recepies_instructions'

class RelationUserMeal(models.Model):
    id_relation = models.AutoField(primary_key=True)
    type_of_relation = models.TextField()

    class Meta:
        managed = False
        db_table = 'relation_user_meal'


class UsersMealAdditionals(models.Model):
    table_id = models.AutoField(primary_key=True)
    id_users = models.ForeignKey(UsersLogin, models.DO_NOTHING, db_column='id_users', blank=True, null=True)
    # id_meal = models.IntegerField()
    relation_type = models.ForeignKey(RelationUserMeal, models.DO_NOTHING, db_column='relation_type', blank=True, null=True)
    id_meal = models.ForeignKey(Recepies, models.DO_NOTHING, db_column='id_meal', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'users_meal_additionals'

#         ------------------------------------------------------------------------------
class Components(models.Model):
    component_uid = models.UUIDField(primary_key=True)
    component_id = models.IntegerField()
    component_name = models.TextField(blank=True, null=True)
    component_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components'


class ComponentsTranslations(models.Model):
    item_uid = models.ForeignKey(Components, models.DO_NOTHING, db_column='item_uid', blank=True, null=True)
    language_code = models.ForeignKey('Languages', models.DO_NOTHING, db_column='language_code', blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components_translations'


class ItemTranslations(models.Model):
    item_uid = models.UUIDField(primary_key=True)
    language_code = models.TextField()
    translation = models.TextField(blank=True, null=True)
    table_source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_translations'
        unique_together = (('item_uid', 'language_code'),)

class ItemTypesCatalog(models.Model):
    item_type_uid = models.UUIDField()
    item_type_desc = models.TextField(blank=True, null=True)
    upd_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'item_types_catalog'

class ItemsCatalog(models.Model):
    item_uid = models.UUIDField()
    item_desc = models.TextField(blank=True, null=True)
    upd_date = models.DateTimeField()
    item_type_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items_catalog'

class Languages(models.Model):
    language_id = models.IntegerField()
    language_code = models.TextField(primary_key=True)
    language_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'languages'



class MeasureUnitsTranslations(models.Model):
    item_uid = models.ForeignKey(MeasureUnits, models.DO_NOTHING, db_column='item_uid', blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measure_units_translations'

class ProductComponents(models.Model):
    rec_id = models.IntegerField(primary_key=True)
    product_uid = models.ForeignKey('Products', models.DO_NOTHING, db_column='product_uid', blank=True, null=True)
    component_uid = models.ForeignKey(Components, models.DO_NOTHING, db_column='component_uid', blank=True, null=True)
    measure_unit_uid = models.ForeignKey(MeasureUnits, models.DO_NOTHING, db_column='measure_unit_uid', blank=True, null=True)
    item_desc = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    upd_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_components'

class ProductImages(models.Model):
    image_id = models.IntegerField(primary_key=True)
    product_uid = models.ForeignKey('Products', models.DO_NOTHING, db_column='product_uid', blank=True, null=True)
    image_proirity = models.IntegerField(blank=True, null=True)
    image_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_images'


class ProductTags(models.Model):
    product_uid = models.ForeignKey('Products', models.DO_NOTHING, db_column='product_uid', blank=True, null=True)
    tag_name = models.TextField(blank=True, null=True)
    tag_type = models.TextField(blank=True, null=True)
    rec_id = models.IntegerField(primary_key=True)
    tag_uid = models.ForeignKey('Tags', models.DO_NOTHING, db_column='tag_uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_tags'


class ProductTranslations(models.Model):
    item_uid = models.ForeignKey('Products', models.DO_NOTHING, db_column='item_uid', blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_translations'



class RecepiInstructionTranslations(models.Model):
    instruction_uid = models.ForeignKey('RecepiesInstructions', models.DO_NOTHING, db_column='instruction_uid', blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepi_instruction_translations'


class RecepiTags(models.Model):
    rec_id = models.IntegerField(primary_key=True)
    recepi_uid = models.ForeignKey('Recepies', models.DO_NOTHING, db_column='recepi_uid', blank=True, null=True)
    tag_uid = models.ForeignKey('Tags', models.DO_NOTHING, db_column='tag_uid', blank=True, null=True)
    tag_name = models.TextField(blank=True, null=True)
    tag_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepi_tags'


class RecepiTranslations(models.Model):
    item_uid = models.ForeignKey('Recepies', models.DO_NOTHING, db_column='item_uid', blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recepi_translations'

class Tags(models.Model):
    tag_uid = models.UUIDField(primary_key=True)
    tag_name = models.TextField(blank=True, null=True)
    tag_type = models.TextField(blank=True, null=True)
    tag_category = models.ForeignKey('TagsCategory', models.DO_NOTHING, db_column='tag_category', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class TagsCategory(models.Model):
    id_tag_category = models.AutoField(primary_key=True)
    category_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'tags_category'


class TagsTranslations(models.Model):
    item_uid = models.ForeignKey(Tags, models.DO_NOTHING, db_column='item_uid', blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)
    translation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags_translations'


class UsersFoodLog(models.Model):
    id_food_log = models.AutoField(primary_key=True)
    user_uid = models.ForeignKey('UsersLogin', models.DO_NOTHING, db_column='user_uid', blank=True, null=True)
    recipe_uid = models.ForeignKey(Recepies, models.DO_NOTHING, db_column='recipe_uid', blank=True, null=True)
    recipe_weight = models.IntegerField()
    food_time = models.TextField()
    date_creation = models.DateField()

    class Meta:
        managed = False
        db_table = 'users_food_log'