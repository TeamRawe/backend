from rest_framework import serializers
from .models import *

class ContactFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFace
        fields = ['id', 'phone', 'email', 'name']
        read_only_fields = ['id']


class SubContractorSerializer(serializers.ModelSerializer):
    # Сериализуем ManyToMany связь с ContactFace
    contacts = ContactFaceSerializer(many=True, read_only=True)

    class Meta:
        model = SubContractor
        fields = ['id', 'title', 'inn', 'ogrn', 'phone', 'email', 'contacts']
        read_only_fields = ['id']


class GovernmentalCompanySerializer(serializers.ModelSerializer):
    # Сериализуем ManyToMany связь с ContactFace
    contacts = ContactFaceSerializer(many=True, read_only=True)

    class Meta:
        model = GovernmentalCompany
        fields = [
            'id', 'title', 'address', 'okfs', 'okopf', 'okogu', 'inn', 'ogrn',
            'kpp', 'okato', 'okpo', 'oktmo', 'phone', 'email', 'website', 'contacts'
        ]
        read_only_fields = ['id']