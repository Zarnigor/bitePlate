from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('table_id', models.UUIDField()),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_phone', models.CharField(blank=True, max_length=30)),
                ('party_size', models.PositiveIntegerField()),
                ('reserved_at', models.DateTimeField()),
                ('status', models.CharField(
                    choices=[
                        ('pending','Pending'),('confirmed','Confirmed'),
                        ('arrived','Arrived'),('no_show','No Show'),('cancelled','Cancelled'),
                    ],
                    default='pending', max_length=20,
                )),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reminder_sent', models.BooleanField(default=False)),
            ],
            options={'ordering': ['reserved_at']},
        ),
    ]
