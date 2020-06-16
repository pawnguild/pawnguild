# Generated by Django 3.0.5 on 2020-06-16 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawnlisting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pawn',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pawn',
            name='primary_inclination',
            field=models.CharField(choices=[('Scather', 'Scather'), ('Medicant', 'Medicant'), ('Mitigator', 'Mitigator'), ('Challenger', 'Challenger'), ('Utilitarian', 'Utilitarian'), ('Guardian', 'Guardian'), ('Nexus', 'Nexus'), ('Pioneer', 'Pioneer'), ('Acquisitor', 'Acquisitor')], max_length=30),
        ),
        migrations.AlterField(
            model_name='pawn',
            name='secondary_inclination',
            field=models.CharField(choices=[('Scather', 'Scather'), ('Medicant', 'Medicant'), ('Mitigator', 'Mitigator'), ('Challenger', 'Challenger'), ('Utilitarian', 'Utilitarian'), ('Guardian', 'Guardian'), ('Nexus', 'Nexus'), ('Pioneer', 'Pioneer'), ('Acquisitor', 'Acquisitor'), ('None', 'None')], max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='pawn',
            unique_together={('id', 'primary_inclination', 'secondary_inclination')},
        ),
    ]
