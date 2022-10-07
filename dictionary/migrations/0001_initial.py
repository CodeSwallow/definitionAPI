# Generated by Django 4.1 on 2022-08-13 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_of_speech', models.CharField(max_length=255)),
                ('definition', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Synonym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('definition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synonyms', to='dictionary.definition')),
            ],
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.CharField(max_length=255)),
                ('definition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examples', to='dictionary.definition')),
            ],
        ),
        migrations.AddField(
            model_name='definition',
            name='word_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', to='dictionary.word'),
        ),
        migrations.CreateModel(
            name='Antonym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('definition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='antonyms', to='dictionary.definition')),
            ],
        ),
    ]
