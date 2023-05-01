from django.db import models
from slugify import slugify


class Skill(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Subject(models.Model):
    university = models.ForeignKey(
        'university.University', on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='subjects')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'subject {self.title} from {self.university}'
