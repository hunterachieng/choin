<<<<<<< HEAD
# Generated by Django 3.2.4 on 2021-11-11 09:56
=======
# Generated by Django 3.2.8 on 2021-11-09 14:41
>>>>>>> febf040e857eed603df4c730ce503df36c358139

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leadership', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redeem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_purchase', models.DateField(null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('complete', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RewardedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.redeem')),
                ('reward', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leadership.redeemableitem')),
            ],
        ),
        migrations.AddField(
            model_name='redeem',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]
