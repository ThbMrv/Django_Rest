from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('concession', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concessionnaire',
            name='siret',
            field=models.CharField(
                help_text='SIRET (14 chiffres), généré automatiquement pour les créations API',
                max_length=14,
                validators=[django.core.validators.RegexValidator(regex='^\\d{14}$', message='Le SIRET doit contenir exactement 14 chiffres.')],
            ),
        ),
    ]
