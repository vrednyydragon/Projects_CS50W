# Generated by Django 3.0.8 on 2020-07-10 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(blank=True, null=True)),
                ('attribute_name', models.TextField(blank=True, null=True)),
                ('attribute_sizing', models.TextField(blank=True, null=True)),
                ('attribute_val', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'item_attributes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(blank=True, null=True)),
                ('image_proirity', models.IntegerField(blank=True, null=True)),
                ('image_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'item_images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ItemTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(blank=True, null=True)),
                ('tag_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'item_tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recepies',
            fields=[
                ('recepi_uid', models.UUIDField(primary_key=True, serialize=False)),
                ('recepi_id', models.IntegerField(blank=True, null=True)),
                ('recepi_name', models.TextField(blank=True, null=True)),
                ('recepi_src_url', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'recepies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RecepiesIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepi_id', models.IntegerField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('ingredient_desc', models.TextField(blank=True, null=True)),
                ('ingredient_amount', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'recepies_ingredients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RecepiesInstructions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepi_id', models.IntegerField(blank=True, null=True)),
                ('step_number', models.IntegerField(blank=True, null=True)),
                ('step_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'recepies_instructions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersLogin',
            fields=[
                ('id_users', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=10)),
                ('date_of_creation', models.DateTimeField()),
            ],
            options={
                'db_table': 'users_login',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id_profile', models.OneToOneField(db_column='id_profile', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='hf_website.UsersLogin')),
                ('date_of_birth', models.DateField()),
                ('gender', models.TextField()),
                ('user_height', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('user_weight', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('type_of_food', models.TextField()),
                ('activity_level', models.DecimalField(decimal_places=65535, max_digits=65535)),
            ],
            options={
                'db_table': 'users_profile',
                'managed': False,
            },
        ),
    ]
