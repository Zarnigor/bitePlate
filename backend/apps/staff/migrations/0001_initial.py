from django.db import migrations, models
import uuid
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=150, unique=True,
                    validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(
                    choices=[
                        ('waiter','Waiter'),('chef','Chef'),
                        ('cashier','Cashier'),('manager','Manager'),
                    ],
                    default='waiter', max_length=20,
                )),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('groups', models.ManyToManyField(blank=True, related_name='staff_member_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='staff_member_set', to='auth.permission')),
            ],
            options={'verbose_name': 'user', 'verbose_name_plural': 'users', 'abstract': False},
            managers=[('objects', django.contrib.auth.models.UserManager())],
        ),
    ]
