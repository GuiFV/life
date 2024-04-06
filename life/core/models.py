from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from life.core import services


class Goal(models.Model):

    PROJECT, TRIP, BUY, DO = 'pr', 'tr', 'by', 'do'
    TYPES = ((PROJECT, 'Project'), (TRIP, 'Trip'), (BUY, 'Buy'), (DO, 'Do'))

    HIGH, LOW = 'hi', 'lo'
    EFFORTS = ((HIGH, 'High'), (LOW, 'Low'))

    PERSONAL, PROFESSIONAL = 'pe', 'pr'
    AREAS = ((PERSONAL, 'Personal'), (PROFESSIONAL, 'Professional'))

    PRIORITIES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    type = models.CharField(max_length=2, choices=TYPES)
    effort = models.CharField(max_length=2, choices=EFFORTS)
    area = models.CharField(max_length=2, choices=AREAS, default=PERSONAL)
    important = models.PositiveSmallIntegerField(choices=PRIORITIES, default='1')
    urgent = models.PositiveSmallIntegerField(choices=PRIORITIES, default='1')
    matrix = models.PositiveSmallIntegerField(default=0)

    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.matrix = self.matrix_calculation()
        return super(Goal, self).save(*args, **kwargs)

    def matrix_calculation(self):
        matrix = self.important * self.urgent
        return matrix

    def __str__(self):
        return self.name


class GoogleAgenda(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agenda_id = models.TextField()
    agenda_clean = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.agenda_clean = services.extract_src_ctz(self.agenda_id)
        return super(GoogleAgenda, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s Google agenda"


class Notes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    my_notes = CKEditor5Field(null=True, blank=True)

    def __str__(self):
        return f"{self.user}'s Notes"

    class Meta:
        verbose_name_plural = 'Notes'
