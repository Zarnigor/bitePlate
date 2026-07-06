from django.db import migrations, models
import uuid
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('order_id', models.UUIDField(unique=True)),
                ('table_id', models.UUIDField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('tax_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tip_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pricing_strategy', models.CharField(default='Standard', max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('split_count', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
