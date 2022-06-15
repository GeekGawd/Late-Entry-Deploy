from django.db import IntegrityError
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from Core.models import Batch, Student , Venue
from Core.models import LateEntry
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# ---------Serializers--------
from Core.serializers import StudentRecordSerializer, CacheSerializer, VenueSerializer

class Scan(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data=request.data
        valid = Student.objects.late_entry_valid(data)
        django_file_validation = Student.objects.validation(settings.DJANGO_CONTEXT_VALIDATOR, data)

        try:
            Student.objects.get(student_no=data.get('student_no'))
        except ObjectDoesNotExist:
            return Response(status=459)

        if not valid:
            return Response(status=462)
            
        if data.get('venue') is None:
            return Response(status=461)
            
        try:
            if django_file_validation:
                LateEntry.objects.create(student_id=data['student_no'],timestamp=data['timestamp'], venue_id=data['venue'])
            return Response(status=261)
        except IntegrityError:
            return Response(status=460)


# class Bulk(APIView):
#     def post(self, request, format=None):
#         data=request.data
#         # already registered entries
#         exists_list = list(LateEntry.objects.filter(timestamp__date=timezone.now()).values_list("student_id", flat=True))
#         print(exists_list)
#         # entered data
#         entry_list = data['student_no']
#         print(entry_list)
#         # not already registered students
#         valid_list = list(set(entry_list)-set(exists_list))
#         print(valid_list)
#         dates = data['date']
#         current = timezone.now()
#         objs = []
#         for student_no in valid_list:
#             if "venue" in data:
#                 if student_no in dates:
#                     # check if future date is not entered
#                     if dt.fromisoformat(dates[student_no])<=current:
#                         objs.append(LateEntry(student_id=student_no,timestamp=dates[str(student_no)], venue_id=data['venue']))
#                     else:
#                         # print("Futue date entered")
#                         valid_list.remove(student_no)
#                         continue
#                 else:
#                     # no date is present
#                     objs.append(LateEntry(student_id=student_no,venue_id=data['venue']))
#             else:
#                 return Response(status=461)
#         success = len(LateEntry.objects.bulk_create(objs=objs, ignore_conflicts=True))
#         failed = len(entry_list)-success
#         return Response({'message':f'{success} Late entries registered {failed} failed. Student number list {valid_list}',
#                         "result": {"success":success,"failed":failed,"data":valid_list},
#                         "status": True,
#                         "status_code": 201},
#                         status=status.HTTP_201_CREATED)

class Bulk(generics.GenericAPIView,
           mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        entries = request.data['entry']
        buffer = 0
        student_entries = []
        for data in entries:
            django_file_validation = Student.objects.validation(settings.DJANGO_CONTEXT_VALIDATOR, data)
            if Student.objects.late_entry_valid(data):
                if django_file_validation:
                    student_entries.append(LateEntry(student_id=data['student_no'],timestamp=data['timestamp'],\
                                venue_id=data['venue']))
                else:
                    buffer +=1
        success = len(LateEntry.objects.bulk_create(objs=student_entries, ignore_conflicts=True)) + buffer
        failed = len(entries)-success
        return Response({'message':f'{success} Late entries registered {failed} failed.',
                        "result": {"success":success,"failed":failed},
                        "status": True,
                        "status_code": 201},
                        status=status.HTTP_201_CREATED)
        


class Cache(generics.ListAPIView):
    serializer_class = CacheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_batch = Batch.objects.last()
        return Student.objects.filter(batch__batch__gte=(current_batch.batch-4))

class GetVenue(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VenueSerializer
    
class NestedStudentVenueView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        current_batch = Batch.objects.last()
        qs_student = Student.objects.filter(batch__batch__gte=(current_batch.batch-4))
        qs_venue = Venue.objects.filter(state=True)

        student_data = CacheSerializer(qs_student, many=True).data
        venue_data = VenueSerializer(qs_venue, many=True).data

        return Response({"venue_data": venue_data, "student_data": student_data})     
