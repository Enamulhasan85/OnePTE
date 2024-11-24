# Generated by Django 5.1.3 on 2024-11-22 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pte_exam', '0005_remove_rmmcqanswer_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rmmcqanswer',
            name='answer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rmmcq_answer_details', to='pte_exam.answer'),
        ),
        migrations.AlterField(
            model_name='roanswer',
            name='answer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ro_answer_details', to='pte_exam.answer'),
        ),
        migrations.AlterField(
            model_name='sstanswer',
            name='answer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sst_answer_details', to='pte_exam.answer'),
        ),
    ]