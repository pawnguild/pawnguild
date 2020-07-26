from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone
from django.conf import settings

from datetime import datetime, timedelta

vocations = ["Fighter", "Warrior", "Strider", "Ranger", "Mage", "Sorcerer"]
genders = ["Male", "Female"]
inclinations = ["Scather", "Medicant", "Mitigator", "Challenger", "Utilitarian", "Guardian", "Nexus", "Pioneer", "Acquisitor"]


def build_choices(l):
    return [(choice, choice) for choice in l]


# Create your models here.

class Pawn(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=30)

    vocation = models.CharField(max_length=20, choices=build_choices(vocations))
    level = models.IntegerField()
    gender = models.CharField(max_length=10, choices=build_choices(genders))

    PRIMARY_INCLINATION_CHOICES = build_choices(inclinations)
    SECONDARY_INCLINATION_CHOICES = PRIMARY_INCLINATION_CHOICES[:] + [("None", "None")]

    primary_inclination = models.CharField(max_length=30, choices=PRIMARY_INCLINATION_CHOICES)
    secondary_inclination= models.CharField(max_length=30, choices=SECONDARY_INCLINATION_CHOICES, default="None")
    tertiary_inclination= models.CharField(max_length=30, choices=SECONDARY_INCLINATION_CHOICES, default="None")

    notes = models.TextField(max_length=1000, blank=True)
    picture = models.ImageField(upload_to="pawn_pictures/", null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(default=timezone.now)

    primary_skills = models.CharField(max_length=100, blank=True)
    secondary_skills = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        super(Pawn, self).save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.level not in range(201):
            errors["level"] = ValidationError('Level must be within 1-200')

        inclinations = {self.primary_inclination, self.secondary_inclination, self.tertiary_inclination}
        if len(inclinations) != 3 and not (self.secondary_inclination == "None" and self.tertiary_inclination == "None"):
            errors["primary_inclination"] = ValidationError("Inclinations must all be different")

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name

    @property
    def activity(self):
        """ Return number of stars that should display in pawn list. No stars after 4 weeks"""
        time_since_modified = timezone.now() - self.last_modified
        weeks_since_modified = time_since_modified.days // 7 
        return 4 - weeks_since_modified

    @property
    def vocation_color(self):
        if self.vocation == "Fighter" or self.vocation == "Warrior":
            return "red"
        elif self.vocation == "Strider" or self.vocation == "Ranger":
            return "yellow"
        else:
            return "blue"

    @property
    def inclination_string(self):
        ret = self.primary_inclination
        if self.secondary_inclination != "None":
            ret += f"/{self.secondary_inclination}"
        if self.tertiary_inclination != "None":
            ret += f"/{self.tertiary_inclination}"
        return ret

    @property
    def pawn_url(self):
        return self.get_absolute_url()


class SteamPawn(Pawn):
    steam_url = models.CharField(max_length=150, blank=False, null=False)

    def get_absolute_url(self):
        return reverse("view-steam-pawn", kwargs={"pk": self.id})


class SwitchPawn(Pawn):
    friend_account_id = models.CharField(max_length=30, blank=False, null=False)
    pawn_id = models.CharField(max_length=30, blank=False, null=False)

    def get_absolute_url(self):
        return reverse("view-switch-pawn", kwargs={"pk": self.id})

class XboxOnePawn(Pawn):
    gamertag = models.CharField(max_length=15)

    def get_absolute_url(self):
        return reverse("view-xbox1-pawn", kwargs={"pk": self.pk})


class PS4Pawn(Pawn):
    psn = models.CharField(max_length=16)

    class Meta:
        verbose_name = "PS4Pawn"
        verbose_name_plural = "PS4 Pawns"

    def get_absolute_url(self):
        return reverse("view-ps4-pawn", kwargs={"pk": self.pk})
    
    
class PS3Pawn(Pawn):
    psn = models.CharField(max_length=16)
    version = models.TextField(max_length=20, choices=build_choices(["DD", "Dark Arisen"]))

    class Meta:
        verbose_name = "PS3Pawn"
        verbose_name_plural = "PS3 Pawns"

    def get_absolute_url(self):
        return reverse("view-ps3-pawn", kwargs={"pk": self.pk})