# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Gamemaster(models.Model):
    spieler_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'gamemaster'


class GamemasterVerwaltetSpot(models.Model):
    spieler_id = models.IntegerField(primary_key=True)
    spot_id = models.IntegerField()
    datum = models.DateTimeField()
    aktion = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gamemaster_verwaltet_spot'
        unique_together = (('spieler_id', 'spot_id'),)


class Medium(models.Model):
    medium_id = models.AutoField(primary_key=True)
    dateityp = models.CharField(max_length=5)
    erstelldatum = models.DateTimeField()
    link = models.CharField(max_length=255)
    profilbild_flag = models.IntegerField()
    spieler_id = models.IntegerField()
    spot_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'medium'


class Ort(models.Model):
    ort_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    plz = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'ort'


class Schwierigkeit(models.Model):
    schwierigkeit_id = models.AutoField(primary_key=True)
    punkte = models.IntegerField()
    beschreibung = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'schwierigkeit'


class Spieler(AbstractUser):
    spieler_id = models.AutoField(primary_key=True)
    nachname = models.CharField(max_length=45)
    vorname = models.CharField(max_length=45)
    punktzahl = models.IntegerField(blank=True, null=True)
    team_id = models.IntegerField()
    ort_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spieler'


class SpielerBewertetSpot(models.Model):
    spieler_id = models.IntegerField(primary_key=True)
    bewertung = models.IntegerField()
    spot_id = models.IntegerField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'spieler_bewertet_spot'
        unique_together = (('spieler_id', 'spot_id'),)


class SpielerEntdecktSpot(models.Model):
    spieler_id = models.IntegerField(primary_key=True)
    spot_id = models.IntegerField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'spieler_entdeckt_spot'
        unique_together = (('spieler_id', 'spot_id'),)


class Spot(models.Model):
    spot_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=8)
    bezeichnung = models.CharField(max_length=45)
    beschreibung = models.CharField(max_length=255)
    laengengrad = models.CharField(max_length=20)
    breitengrad = models.CharField(max_length=20)
    bewertung = models.IntegerField(blank=True, null=True)
    ort_id = models.IntegerField()
    schwierigkeit_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'spot'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'team'
