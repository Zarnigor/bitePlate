from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('table_id', models.UUIDField()),
                ('staff_id', models.UUIDField()),
                ('status', models.CharField(
                    choices=[
                        ('draft','Draft'),('confirmed','Confirmed'),
                        ('in_kitchen','In Kitchen'),('served','Served'),
                        ('awaiting_bill','Awaiting Bill'),('cancelled','Cancelled'),('closed','Closed'),
                    ],
                    default='draft', max_length=20,
                )),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('order', models.ForeignKey(
                    on_delete=models.deletion.CASCADE,
                    related_name='items',
                    to='orders.order',
                )),
                ('menu_item_id', models.UUIDField()),
                ('menu_item_name', models.CharField(max_length=200)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('special_notes', models.TextField(blank=True)),
            ],
        ),
    ]
