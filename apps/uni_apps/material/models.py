from django.db import models


class Lecture(models.Model):
    subject = models.ForeignKey(
        'subject.Subject', on_delete=models.CASCADE, related_name='lectures')
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return self.title


class LectureFile(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='materials')

    class Meta:
        verbose_name = 'Файл лекции'
        verbose_name_plural = 'Файлы лекции'

    def __str__(self):
        return f"{self.file.name} on {self.lecture.title}"
