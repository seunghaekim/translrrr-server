# Generated by Django 3.0.3 on 2020-02-14 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentsHash',
            fields=[
                ('seq', models.AutoField(primary_key=True, serialize=False)),
                ('contents_hash', models.CharField(db_index=True, max_length=255, unique=True)),
                ('updatetime', models.DateTimeField(auto_now=True, null=True)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentsCache',
            fields=[
                ('seq', models.AutoField(primary_key=True, serialize=False)),
                ('translated_text', models.TextField()),
                ('vendor', models.CharField(max_length=16)),
                ('source', models.CharField(max_length=8)),
                ('target', models.CharField(max_length=8)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('contents_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translator.ContentsHash')),
            ],
        ),
    ]
