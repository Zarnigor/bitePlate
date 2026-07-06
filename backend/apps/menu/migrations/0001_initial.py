from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('category', models.CharField(
                    choices=[
                        ('starter','Starter'),('main','Main Course'),
                        ('dessert','Dessert'),('beverage','Beverage'),
                    ],
                    max_length=20,
                )),
                ('is_available', models.BooleanField(default=True)),
                ('prep_time_seconds', models.PositiveIntegerField(default=600)),
                ('cooking_station', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['category', 'name']},
        ),
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('menu_item', models.ForeignKey(
                    on_delete=models.deletion.CASCADE,
                    related_name='allergens',
                    to='menu.menuitem',
                )),
            ],
        ),
        migrations.CreateModel(
            name='ComboMeal',
            fields=[
                ('menuitem_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='menu.menuitem',
                )),
                ('discount_pct', models.DecimalField(
                    decimal_places=2, default='10.00',
                    help_text='Discount percentage applied to sum of item prices.',
                    max_digits=5,
                )),
                ('items', models.ManyToManyField(
                    blank=True,
                    related_name='combo_meals',
                    to='menu.menuitem',
                )),
            ],
            bases=('menu.menuitem',),
        ),
    ]
