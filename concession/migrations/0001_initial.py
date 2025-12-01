from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Concessionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=64)),
                ('siret', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('moto', 'Moto'), ('auto', 'Auto')], max_length=4)),
                ('marque', models.CharField(max_length=64)),
                ('chevaux', models.IntegerField()),
                ('prix_ht', models.FloatField()),
                ('concessionnaire', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='vehicules', to='concession.concessionnaire')),
            ],
        ),
    ]
