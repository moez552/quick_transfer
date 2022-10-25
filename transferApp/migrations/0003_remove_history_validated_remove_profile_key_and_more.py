# Generated by Django 4.1.2 on 2022-10-20 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transferApp', '0002_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='validated',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='key',
        ),
        migrations.AddField(
            model_name='history',
            name='status',
            field=models.CharField(choices=[('PN', 'Pending'), ('SS', 'Success'), ('FL', 'Fail')], default=('PN', 'Pending'), max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]