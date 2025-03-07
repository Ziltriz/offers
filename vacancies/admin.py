from django.contrib import admin
from vacancies.models import Profession, Vacancy, VacancyKeyWords

# Регистрация модели Profession
@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'search_query')  # Поля, отображаемые в списке
    search_fields = ('name',)  # Поля, по которым можно искать
    list_filter = ('name',)  # Фильтры в правой панели

# Регистрация модели VacancyKeyWords
@admin.register(VacancyKeyWords)
class VacancyKeyWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Поля, отображаемые в списке
    search_fields = ('name',)  # Поля, по которым можно искать
    list_filter = ('name',)  # Фильтры в правой панели

# Регистрация модели Vacancy
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'profession', 'published_at')  # Поля, отображаемые в списке
    search_fields = ('title', 'profession__name')  # Поля, по которым можно искать
    list_filter = ('profession', 'published_at')  # Фильтры в правой панели
    filter_horizontal = ('key_skills',)  # Удобный виджет для выбора ключевых навыков