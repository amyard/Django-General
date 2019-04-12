from django.db import models
from projects.models import Project
from django.utils import timezone



class Task(models.Model):

    HIGN = 1
    MIDDLE = 0
    LOW = -1
    PRIORITY = ((HIGN, 'Hign'),(MIDDLE, 'Middle'),(LOW, 'Low'))

    COMPLETED = 1
    UNCOMPLETED = 0
    STATUS = ((COMPLETED, 'Completed'),(UNCOMPLETED, 'Uncompleted'))

    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'project')
    title = models.CharField(max_length = 255)
    priority = models.IntegerField(choices = PRIORITY)
    description = models.TextField()
    status = models.IntegerField(choices = STATUS, default = UNCOMPLETED)
    timestamp = models.DateField(blank = True, default = timezone.now)

    def __str__(self):
        return f'{self.title}'