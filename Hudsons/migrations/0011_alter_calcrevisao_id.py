# Generated by Django 5.1.4 on 2024-12-21 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hudsons', '0010_delete_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calcrevisao',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
