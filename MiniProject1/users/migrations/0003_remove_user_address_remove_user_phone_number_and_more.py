# Generated by Django 5.1.6 on 2025-02-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_address_user_phone_number_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('trader', 'Trader'), ('sales_rep', 'Sales Representative'), ('customer', 'Customer')], max_length=20),
        ),
    ]
