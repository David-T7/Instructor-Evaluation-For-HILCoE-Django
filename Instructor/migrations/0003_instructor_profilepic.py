# Generated by Django 4.2.7 on 2023-11-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0002_instructor_title_alter_instructor_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='ProfilePic',
            field=models.FileField(blank=True, default='profilepic/defaultprofile.jpeg', null=True, upload_to='profilepic/'),
        ),
    ]
