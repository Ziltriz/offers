from django.db import models

class Profession(models.Model):
    name = models.CharField(max_length=255)
    search_query = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VacancyKeyWords(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='vacancies')
    vacancy_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    key_skills = models.ManyToManyField(VacancyKeyWords)
    published_at = models.DateTimeField()
    json_data = models.JSONField()

    def __str__(self):
        return self.title