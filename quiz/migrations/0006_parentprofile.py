from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0005_student_unlocked_avatars'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='parent_profile',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('children', models.ManyToManyField(
                    blank=True,
                    help_text='Student accounts this parent is linked to',
                    related_name='parents',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
    ]
