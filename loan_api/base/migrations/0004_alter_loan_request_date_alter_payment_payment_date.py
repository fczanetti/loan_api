# Generated by Django 5.0.7 on 2024-07-19 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_loan_value_alter_payment_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='request_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(blank=True),
        ),
    ]
