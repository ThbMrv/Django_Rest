from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('concession', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concessionnaire',
            name='owner',
            field=models.ForeignKey(blank=True, help_text="Utilisateur ayant créé ce concessionnaire (ne pas exposer via l'API)", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='concessions', to=settings.AUTH_USER_MODEL),
        ),
    ]
