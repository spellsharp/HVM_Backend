# Generated by Django 4.2.6 on 2023-10-18 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hvm', '0007_leadvisitor_valid_till'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('full_name', models.CharField(max_length=200)),
                ('employee_id', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]