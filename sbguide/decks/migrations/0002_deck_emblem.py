# Generated by Django 2.2 on 2019-04-25 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20190424_2146'),
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='emblem',
            field=models.ForeignKey(default=37363, on_delete=django.db.models.deletion.CASCADE, related_name='emblem_card', to='cards.Card'),
            preserve_default=False,
        ),
    ]
