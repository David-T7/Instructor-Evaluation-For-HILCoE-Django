# Generated by Django 4.2.7 on 2023-12-04 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0013_alter_term_evaluation_end_date_and_more'),
        ('Student', '0013_alter_student_batch'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('Student_id', 'Batch')},
        ),
    ]