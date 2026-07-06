from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=__import__('uuid').uuid4, editable=False, serialize=False)),
                ('number', models.PositiveIntegerField(unique=True)),
                ('capacity', models.PositiveIntegerField(default=4)),
                ('status', models.CharField(
                    choices=[
                        ('free','Free'),('reserved','Reserved'),('occupied','Occupied'),
                        ('awaiting_bill','Awaiting Bill'),('cleared','Cleared'),
                    ],
                    default='free', max_length=20,
                )),
                ('location', models.CharField(blank=True, max_length=100)),
            ],
            options={'ordering': ['number']},
        ),
    ]
