# Generated by Django 4.1.4 on 2022-12-16 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]