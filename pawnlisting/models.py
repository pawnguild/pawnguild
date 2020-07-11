from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

from crum import get_current_user

from django.utils import timezone

from datetime import datetime, timedelta

vocations = ["Fighter", "Warrior", "Strider", "Ranger", "Mage", "Sorcerer"]
genders = ["Male", "Female"]
inclinations = ["Scather", "Medicant", "Mitigator", "Challenger", "Utilitarian", "Guardian", "Nexus", "Pioneer", "Acquisitor"]

def build_choices(l):
    return [(choice, choice) for choice in l]

# Create your models here.

class Pawn(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=30)

    vocation = models.CharField(max_length=20, choices=build_choices(vocations))
    level = models.IntegerField()
    gender = models.CharField(max_length=10, choices=build_choices(genders))

    PRIMARY_INCLINATION_CHOICES = build_choices(inclinations)
    SECONDARY_INCLINATION_CHOICES = PRIMARY_INCLINATION_CHOICES[:] + [("None", "None")]

    primary_inclination = models.CharField(max_length=30, choices=PRIMARY_INCLINATION_CHOICES)
    secondary_inclination= models.CharField(max_length=30, choices=SECONDARY_INCLINATION_CHOICES)


    notes = models.TextField(max_length=1000, blank=True)
    picture = models.ImageField(upload_to="pawn_pictures/", null=True, blank=True)

    created_by = models.ForeignKey("auth.User", default=None, null=False, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(default=timezone.now)

    @property
    def activity(self):
        """ Return number of stars that should display in pawn list. No stars after 4 weeks"""
        time_since_modified = timezone.now() - self.last_modified
        weeks_since_modified = time_since_modified.days % 7 
        return 4 - weeks_since_modified

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            raise ValidationError("User not logged in, anonymous user")
        self.created_by = user

        self.last_modified = timezone.now()

        super(Pawn, self).save(*args, **kwargs)


    def clean(self):
        errors = {}
        if self.level not in range(201):
            errors["level"] = ValidationError('Level must be within 1-200')
        if self.primary_inclination == self.secondary_inclination:
            errors["secondary_inclination"] = ValidationError('Primary and secondary inclinations should be different.')

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse("view_pawn", kwargs={"pk": self.id})
    

    def __str__(self):
        return self.name