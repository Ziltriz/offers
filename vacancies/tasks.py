import requests
from datetime import datetime
from celery import shared_task
from vacancies.models import Profession, Vacancy, VacancyKeyWords
from vacancies.client_hh import HHClient
from django.http import JsonResponse

@shared_task
def fetch_vacancies_for_profession(profession_id):
    client = HHClient('VacancyAnalyzerZiltrizTest/1.0 (support@vacancyanalyzer.com)')
    profession = Profession.objects.get(id=profession_id)

    query = str(profession.search_query)
    vacancies = client.fetch_vacancies(search_query=query, per_page=10)
    if vacancies is None:
        return False

    for vacancy_data in vacancies:
        vacancy_id = vacancy_data.get('id')
        title = vacancy_data.get('name')
        published_at = datetime.strptime(vacancy_data.get('published_at'), '%Y-%m-%dT%H:%M:%S%z')
        json_data = vacancy_data

        vacancy, created = Vacancy.objects.get_or_create(
            vacancy_id=vacancy_id,
            defaults={
                'profession': profession,
                'title': title,
                'published_at': published_at,
                'json_data': json_data
            }
        )
        
        process_vacancy_details.delay(vacancy_id)
    return True
    

@shared_task
def process_vacancy_details(vacancy_id: str):
    """
    Задача для обработки деталей вакансии и обновления ключевых навыков.
    
    :param vacancy_id: ID вакансии.
    """
    # Получаем вакансию из базы данных
    try:
        vacancy = Vacancy.objects.get(vacancy_id=vacancy_id)
    except Vacancy.DoesNotExist:
        print(f"Вакансия с ID {vacancy_id} не найдена.")
        return

    # Используем клиент для работы с API HH.ru
    client = HHClient(user_agent="VacancyAnalyzer/1.0 (support@vacancyanalyzer.com)")
    vacancy_details = client.fetch_vacancy_details(vacancy_id)

    if vacancy_details is None:
        print(f"Не удалось получить детали вакансии с ID {vacancy_id}.")
        return

    # Обновляем ключевые навыки
    if 'key_skills' in vacancy_details:
        for skill in vacancy_details['key_skills']:
            skill_name = skill.get('name')
            skill_obj, created = VacancyKeyWords.objects.get_or_create(name=skill_name)
            vacancy.key_skills.add(skill_obj)

    print(f"Ключевые навыки для вакансии {vacancy_id} успешно обновлены.")