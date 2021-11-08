# Generated by Django 3.2.8 on 2021-11-06 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_redeem_rewardeditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='redeem',
            name='complete',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='redeem',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='rewardeditem',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
