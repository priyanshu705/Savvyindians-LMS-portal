from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_fill_null_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                'email address',
                max_length=254,
                unique=True,
                null=False,
                blank=False,
                help_text='Required. Used for login and notifications.'
            ),
        ),
    ]
