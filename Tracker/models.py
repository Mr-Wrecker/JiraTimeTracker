from django.db import models
from django.utils import timezone

# Create your models here.


class Track(models.Model):
    STATUS_CHOICES = (
        ('S', "Start Work On Issue"),
        ('E', "End Work On Issue"),
        ('O', "Other Transition")
    )

    issueId = models.CharField(max_length=50)
    userKey = models.CharField(max_length=50)
    projectKey = models.CharField(max_length=50)
    transitionStatus = models.CharField(max_length=1, choices=STATUS_CHOICES)
    transitionTime = models.DateTimeField(default=timezone.now)
    isLastTransition = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.issueId} {self.userKey}"
