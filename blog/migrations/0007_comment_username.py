# Generated by Django 4.2 on 2023-05-25 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_postmark_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
