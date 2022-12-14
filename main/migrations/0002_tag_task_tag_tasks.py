# Generated by Django 4.1.2 on 2022-10-14 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField()),
                ('priority', models.IntegerField(default=1)),
                ('state', models.CharField(choices=[('new_task', 'New'), ('in_development', 'Development'), ('in_qa', 'Qa'), ('in_code_review', 'Code Review'), ('ready_for_release', 'Ready For Release'), ('released', 'Released'), ('archived', 'Archived')], default='new_task', max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='executor', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='main.tag')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='tasks',
            field=models.ManyToManyField(to='main.task'),
        ),
    ]
