# Generated by Django 3.2.8 on 2021-11-08 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_alter_rewardeditem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rewardeditem',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
