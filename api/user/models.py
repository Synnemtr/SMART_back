from django.db import models
from django.contrib.auth.models import AbstractUser
from api.user.managers import UserManager, ProfileManager

SEX_CHOICES = (
    ("MAN", "Man"),
    ("WOMAN", "Woman"),
    ("OTHER", "Other"),
)
FITNESS_GOAL_CHOICES = (
    (1, 'Lose Weight'),
    (2, 'Build Muscle'),
    (3, 'Improve Endurance'),
    (4, 'Get Stronger'),
    (5, 'Stay Fit and Healthy'),
    (6, 'Other'),
)
HEXADTYPES_CHOICES = (
    (  0, "Philanthropist"),
    (  1, "Socialiser"),
    (  2, "Free Spirit"),
    (  3, "Achiever"),
    (  4, "Disruptor"),
    (  5, "Player")
)
MOTIVATION_CHOICES = (
    (  0, "Non-Regulation"),
    (  1, "External Regulation"),
    (  2, "Introjected Regulation"),
    (  3, "Identified Regulation"),
    (  4, "Integrated Regulation"),
    (  5, "Intrinsic Motivation")
)
DIET_CHOICES = (
    ('vegetarian', 'Vegetarian'),
    ('vegan', 'Vegan'),
    ('pescatarian', 'Pescatarian'),
    ('keto', 'Keto'),
    ('paleo', 'Paleo'),
    ('gluten_free', 'Gluten-Free'),
    # Add more diet options as needed...
)

class User(AbstractUser):
    class Meta:
        ordering = ["id"]
        db_table = "user_user"
    objects = UserManager()

    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    email = models.EmailField("email address", unique=True, blank=True, null=True)

    phone_number = models.CharField(max_length=255, default='', blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} : {self.username}" if self.username else self.email

    @property
    def full_name(self):
        return self.get_full_name()

    def is_owner(self, id_user):
        return self.id == id_user


class Profile(models.Model):
    class Meta:
        ordering = ["user"]
        db_table = "user_profile"

    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    picture = models.ImageField(null=True, blank=True)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    body_fat = models.FloatField(blank=True, null=True)
    total_points = models.FloatField(blank=True, null=True)
    goal = models.IntegerField(choices=FITNESS_GOAL_CHOICES, blank=True, null=False,default=2)
    sub_goal = models.CharField(max_length=255, blank=True, null=True)
    training_per_week = models.IntegerField(blank=True, null=True)
    preferred_diet = models.CharField(max_length=50, choices=DIET_CHOICES,null=True)
    HEXAD_12_type = models.IntegerField(blank=True, null=True)
    HEXAD_12_sub_type = models.IntegerField(choices=HEXADTYPES_CHOICES , blank=True, null=True)
    motivation_type = models.IntegerField(choices=MOTIVATION_CHOICES , blank=True, null=True)
    current_streak = models.IntegerField(default=1)

    objects = ProfileManager()

    def is_owner(self, id_user):
        return self.user.id == id_user
