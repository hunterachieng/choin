# Generated by Django 3.2.8 on 2021-11-08 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20211106_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeem',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='student.student'),
        ),
    ]