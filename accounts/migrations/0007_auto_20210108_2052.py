# Generated by Django 3.1 on 2021-01-08 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_first_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneotp',
            name='forgot',
            field=models.BooleanField(default=False, help_text='only true for forgot password'),
        ),
        migrations.AddField(
            model_name='phoneotp',
            name='forgot_logged',
            field=models.BooleanField(default=False, help_text='Only true if validate otp forgot is successful'),
        ),
    ]
