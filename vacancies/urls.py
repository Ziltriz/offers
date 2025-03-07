from django.urls import path
from vacancies.views import VacancyList, ProfessionSkillsView
from .views import start_fetch_vacancies


urlpatterns = [
    path('vacancies/', VacancyList.as_view(), name='vacancy-list'),
    path('profession/<int:profession_id>/skills/', ProfessionSkillsView.as_view(), name='profession-skills'),
    path('fetch_vacancies/<int:profession_id>/', start_fetch_vacancies, name='fetch_vacancies'),
]