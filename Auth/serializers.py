from dataclasses import field
from rest_framework import serializers
from Core.models import *
from rest_framework.views import APIView
from . models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class LateEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LateEntry
        fields = ['__all__']

class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']