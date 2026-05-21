from django.db import migrations


def rename_autores_to_bloggers(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')

    old_group = Group.objects.filter(name='autores').first()
    if old_group is None:
        return

    new_group = Group.objects.filter(name='bloggers').first()
    if new_group is None:
        old_group.name = 'bloggers'
        old_group.save(update_fields=['name'])
        return

    new_group.permissions.add(*old_group.permissions.all())
    for user in User.objects.filter(groups=old_group):
        user.groups.add(new_group)
    old_group.delete()


def rename_bloggers_to_autores(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    bloggers_group = Group.objects.filter(name='bloggers').first()
    if bloggers_group is None or Group.objects.filter(name='autores').exists():
        return

    bloggers_group.name = 'autores'
    bloggers_group.save(update_fields=['name'])


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0002_emailsettings'),
    ]

    operations = [
        migrations.RunPython(
            rename_autores_to_bloggers,
            rename_bloggers_to_autores,
        ),
    ]
