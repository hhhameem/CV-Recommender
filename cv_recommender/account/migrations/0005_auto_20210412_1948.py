# Generated by Django 3.1.7 on 2021-04-12 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210411_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='recruiter',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
