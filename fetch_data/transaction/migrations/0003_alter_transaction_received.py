# Generated by Django 4.2.1 on 2023-05-30 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_rename_tr_jtype_transaction_tr_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='received',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
