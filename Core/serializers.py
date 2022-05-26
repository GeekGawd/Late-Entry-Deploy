from rest_framework import serializers
from Core.models import LateEntry
from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Student, Venue
from django.template.defaultfilters import slugify

class LateEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LateEntry
        fields = ['student']

class StudentRecordSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='late_entry_count')
    timestamp = serializers.DateTimeField(source='timestamp_entry')

    class Meta:
        model = Student
        fields = ['student_no','name','count','timestamp']


class StudentIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

class CacheSerializer(serializers.ModelSerializer):
    student_image = serializers.SerializerMethodField()
    branch = serializers.CharField(source="branch.name")
    batch = serializers.CharField(source="batch.batch")

    class Meta:
        model = Student
        fields = '__all__'

    def get_student_image(self, instance):
        try:
            student_img_url = Student.objects.get(student_no=instance.student_no).student_image.url
            return slugify(student_img_url)
        except ObjectDoesNotExist:
            return None
            
class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ['id','venue']