from django.db import migrations


def fill_null_emails(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    db_alias = schema_editor.connection.alias
    # Use a deterministic placeholder unique per user to avoid unique constraint collisions
    users = User.objects.using(db_alias).filter(email__isnull=True) | User.objects.using(db_alias).filter(email='')
    for user in users:
        user.email = f"user{user.pk}@noemail.local"
        user.save(update_fields=['email'])


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_student_options_alter_student_level_and_more'),
    ]

    operations = [
        migrations.RunPython(fill_null_emails, reverse_code=migrations.RunPython.noop),
    ]
