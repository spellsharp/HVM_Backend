# Generated by Django 4.2.6 on 2023-10-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hvm', '0016_alter_leadvisitor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadvisitor',
            name='image',
            field=models.CharField(blank=True, max_length=25000000, null=True),
        ),
    ]
