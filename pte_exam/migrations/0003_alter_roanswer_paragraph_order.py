# Generated by Django 5.1.3 on 2024-11-21 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pte_exam', '0002_rmmcqanswer_roanswer_sstanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roanswer',
            name='paragraph_order',
            field=models.JSONField(help_text='Submitted order of paragraphs.'),
        ),
    ]