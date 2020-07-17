# Generated by Django 3.0.8 on 2020-07-17 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pawnlisting', '0003_auto_20200717_0031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='platform',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='steam_url',
        ),
        migrations.AddField(
            model_name='pawn',
            name='platform',
            field=models.CharField(choices=[('Steam', 'Steam'), ('Switch', 'Switch'), ('XBOne', 'XBOne'), ('PS4', 'PS4'), ('PS3', 'PS3')], default='Steam', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pawn',
            name='teriary_inclination',
            field=models.CharField(choices=[('Scather', 'Scather'), ('Medicant', 'Medicant'), ('Mitigator', 'Mitigator'), ('Challenger', 'Challenger'), ('Utilitarian', 'Utilitarian'), ('Guardian', 'Guardian'), ('Nexus', 'Nexus'), ('Pioneer', 'Pioneer'), ('Acquisitor', 'Acquisitor'), ('None', 'None')], default='None', max_length=30),
        ),
        migrations.AlterField(
            model_name='pawn',
            name='secondary_inclination',
            field=models.CharField(choices=[('Scather', 'Scather'), ('Medicant', 'Medicant'), ('Mitigator', 'Mitigator'), ('Challenger', 'Challenger'), ('Utilitarian', 'Utilitarian'), ('Guardian', 'Guardian'), ('Nexus', 'Nexus'), ('Pioneer', 'Pioneer'), ('Acquisitor', 'Acquisitor'), ('None', 'None')], default='None', max_length=30),
        ),
        migrations.CreateModel(
            name='SwitchPawnProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_code', models.CharField(max_length=30)),
                ('pawn_code', models.CharField(max_length=30)),
                ('pawn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pawnlisting.Pawn')),
            ],
        ),
        migrations.CreateModel(
            name='SteamPawnProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steam_url', models.CharField(max_length=150)),
                ('pawn', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pawnlisting.Pawn')),
            ],
        ),
    ]
