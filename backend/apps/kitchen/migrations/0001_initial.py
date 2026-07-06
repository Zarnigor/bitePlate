from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='KitchenTicket',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('order_id', models.UUIDField()),
                ('order_item_id', models.UUIDField()),
                ('item_name', models.CharField(max_length=200)),
                ('station', models.CharField(default='hot_kitchen', max_length=100)),
                ('status', models.CharField(
                    choices=[
                        ('queued','Queued'),('preparing','Preparing'),
                        ('ready','Ready'),('cancelled','Cancelled'),
                    ],
                    default='queued', max_length=20,
                )),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('special_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['created_at']},
        ),
    ]
