from rest_framework import serializers
from vacancies.models import VacancyKeyWords, Vacancy

class VacancyKeyWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyKeyWords
        fields = ['name']

class VacancySerializer(serializers.ModelSerializer):
    key_skills = VacancyKeyWordsSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = ['title', 'key_skills']

class SkillCountSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()

class VacancySkillCountSerializer(serializers.Serializer):
    title = serializers.CharField()
    skills = SkillCountSerializer(many=True)