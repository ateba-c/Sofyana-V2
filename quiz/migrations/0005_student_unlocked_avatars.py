from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_add_error_type_to_interaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="unlocked_avatars",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
