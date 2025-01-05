# Generated by Django 5.1.4 on 2024-12-17 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hudsons', '0003_alter_calcrevisao_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcrevisao',
            name='data',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='calcrevisao',
            name='diagramacao',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='calcrevisao',
            name='tipo',
            field=models.CharField(choices=[('tcc', 'TCC'), ('dissertacao', 'Dissertação'), ('tese', 'Tese'), ('outros', 'Outros')], max_length=50),
        ),
    ]
