from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import JsonResponse
from .models import Vacancy, VacancyKeyWords, Profession
from .serializers import VacancySerializer, SkillCountSerializer, ProfessionSkillsSerializer
from .tasks import fetch_vacancies_for_profession

class VacancyList(generics.ListAPIView):
    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()

class VacancySkillCountView(APIView):
    def get(self, request):
        profession_id = request.query_params.get('profession_id')
        if profession_id:
            vacancies = Vacancy.objects.filter(profession_id=profession_id).values('title').annotate(total_vacancies=Count('id'))
        else:
            vacancies = Vacancy.objects.values('title').annotate(total_vacancies=Count('id'))

        result = []
        for vacancy in vacancies:
            title = vacancy['title']
            skills = VacancyKeyWords.objects.filter(vacancy__title=title).values('name').annotate(count=Count('id'))
            skill_data = SkillCountSerializer(skills, many=True).data
            result.append({
                'title': title,
                'skills': skill_data
            })

        return Response(result)

def start_fetch_vacancies(request, profession_id):
    # Запускаем задачу асинхронно
    fetch_vacancies_for_profession.delay(profession_id)
    return JsonResponse({"status": "started", "profession_id": profession_id})

class ProfessionSkillsView(APIView):
    def get(self, request, profession_id):
        try:
            profession = Profession.objects.get(id=profession_id)
        except Profession.DoesNotExist:
            return Response({"error": "Profession not found"}, status=404)

        skills = VacancyKeyWords.objects.filter(vacancy__profession=profession).annotate(
            count=Count('vacancy')
        ).values('name', 'count')

        data = {
            "profession": profession.name,
            "skills": skills
        }

        serializer = ProfessionSkillsSerializer(data)
        return Response(serializer.data)