# Generated by Django 4.2.7 on 2023-11-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0005_studentcourseenrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentevaluationresult',
            name='EvaluationDone',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
