from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

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

    def clean(self):
        if self.primary_inclination == self.secondary_inclination:
            raise ValidationError('Primary and secondary inclinations should be different.')


    def get_absolute_url(self):
        return reverse("list_pawn")
    

    def __str__(self):
        return "Name: " + self.name + " Vocation " + self.vocation + " level " + str(self.level) + \
            " Gender " + self.gender + " primary inclination " + self.primary_inclination + " secondary inclination " + self.secondary_inclination