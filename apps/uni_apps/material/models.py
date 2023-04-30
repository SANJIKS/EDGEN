from django.db import models


class Lecture(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='lectures')
    name = models.CharField(max_length=255)
    description = models.TextField()
    files = models.ManyToManyField('LectureFile', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LectureFile(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name='files')
    file = models.FileField()

    def __str__(self):
        return self.file.name
