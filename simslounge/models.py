from django.db import models
from django.contrib.auth.models import User

class Lounge(models.Model):
    lounge_name = models.CharField(max_length=200)
    lounge_description = models.TextField(blank=True, null=True)
    lounge_rep_1 = models.CharField(max_length=200)
    lounge_rep_2 = models.CharField(max_length=200, blank=True, null=True)
    lounge_url = models.URLField(max_length=200, blank=True, null=True)
    lounge_funds = models.IntegerField()
    interlounge_funds = models.IntegerField()

    def __str__(self):
        return self.lounge_name

class LoungeMember(models.Model):
    lounge = models.ForeignKey("Lounge", models.CASCADE, related_name="members")
    resident = models.ForeignKey("Resident", models.CASCADE, related_name="memberships")
    funding = models.IntegerField()

    def __str__(self):
        return self.resident.resident_name + " - " + self.lounge.lounge_name


class Resident(models.Model):
    resident_name = models.CharField(max_length=200)
    resident_title = models.CharField(max_length=200, blank=True, null=True)
    resident_kerb = models.CharField(max_length=20)
    resident_funding = models.IntegerField()
    resident_user = models.OneToOneField(User, models.SET_NULL, related_name="resident", blank=True, null=True)

    def __str__(self):
        return self.resident_name



class Proposal(models.Model):
    proposal_name = models.CharField(max_length=50)
    proposal_description = models.TextField(blank=True, null=True)
    proposal_amount = models.IntegerField()
    proposal_lounge = models.ForeignKey("Lounge", models.CASCADE, related_name="proposals")
    proposal_creator = models.ForeignKey("Resident", models.SET_NULL, null=True)
    proposal_yes = models.ManyToManyField("LoungeMember", related_name="yes_votes", blank=True, null=True)
    proposal_no = models.ManyToManyField("LoungeMember", related_name="no_votes", blank=True, null=True)
    proposal_reg_funding = models.BooleanField()
    proposal_passed = models.BooleanField()

    def __str__(self):
        return self.proposal_name

