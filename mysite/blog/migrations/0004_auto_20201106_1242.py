# Generated by Django 2.2 on 2020-11-06 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_body_preview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date_published',), 'verbose_name': 'статью', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='publish',
            new_name='date_published',
        ),
    ]
