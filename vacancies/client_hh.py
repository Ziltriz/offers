import requests
from typing import List, Dict, Optional

class HHClient:
    
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self, user_agent: str = "MyApp/1.0 (my-app-feedback@example.com)"):
        self.headers = {
            'User-Agent': user_agent,
        }

    def fetch_vacancies(self, search_query: str, per_page: int = 100, page: int = 0) -> Optional[List[Dict]]:
        """
        Получает список вакансий по поисковому запросу.
        
        :param search_query: Поисковый запрос.
        :param per_page: Количество вакансий на странице.
        :param page: Номер страницы.
        :return: Список вакансий или None в случае ошибки.
        """

        params = {
            'per_page': per_page,
            'page': page,
        }

        try:
            response = requests.get(str(self.BASE_URL+search_query), params=params, headers=self.headers)
            response.raise_for_status()  
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API HH.ru: {e}")
            return None

    def fetch_vacancy_details(self, vacancy_id: str) -> Optional[Dict]:
        """
        Получает детали вакансии по её ID.
        
        :param vacancy_id: ID вакансии.
        :return: Детали вакансии или None в случае ошибки.
        """
        url = f"{self.BASE_URL}/{vacancy_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API HH.ru: {e}")
            return None