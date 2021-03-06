from multiprocessing.managers import BaseManager
from django.db import models
from pytz import timezone
from Auth.models import User
from Core.validators import student_no_re, student_name_re, branch_name_re, branch_code_re
from unicodedata import name
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from Auth.models import User
from django.db.models import CheckConstraint, Q
from filer.fields.image import FilerFileField, FilerImageField
from Core.utils import compress
from filer.models.abstract import BaseImage
from filer.models.filemodels import File
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from filer.models import Folder

class StudentManager(models.Manager):
    
    def late_entry_valid(self, data):
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S.%f%z')
        try:
            result = (LateEntry.objects.filter(Q(timestamp__date=timestamp) & 
                            Q(student=Student.objects.get(student_no=data['student_no']))).exists()\
                            or timestamp > timezone.now())
            return not result
        except ObjectDoesNotExist:
                return False
    
    def validation(self, django_file, data):
        django_file = django_file.split('/')
        return not (data.get('student_no') in django_file)

class Operator(User):

    class Meta:
        proxy=True

class Venue(models.Model):
    venue = models.CharField(max_length=20, validators=[branch_name_re()])
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.venue

class Branch(models.Model):
    name = models.CharField(max_length=50, validators=[branch_name_re()])
    active = models.BooleanField(default=True)
    code = models.IntegerField(validators=[branch_code_re()])

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Branches'

class Batch(models.Model):
    batch = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.batch)
    
    def clean(self) -> None:
        if self.batch < 1998:
            raise ValidationError("The Batches cannot be made before college establishment.") 
    
    def save(self, *args, **kwargs):
        Folder.objects.create(name=str(self))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Batches"
        ordering = ['batch',]
        constraints = [
            CheckConstraint(
                check = Q(batch__gt=1997), name="check_batch"
            )
        ]

class Student(models.Model):
    student_no = models.CharField(primary_key=True, max_length=11, validators=[student_no_re()])
    name = models.CharField(max_length=255, validators=[student_name_re()])
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)

    objects = StudentManager()
    
    def late_entry_count(self):
        return self.late_entry.all().count()
    
    def timestamp_entry(self):
        return self.late_entry.all().last().timestamp

    def __str__(self):
        return self.name

class LateEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='late_entry')
    timestamp = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="late_entry")

    class Meta:
        verbose_name_plural = 'Late Entries'
    
    def __str__(self):
        return str(self.student.name)+'_'+str(self.student.student_no)

class CustomImage(BaseImage):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name="student_image")

    class Meta(BaseImage.Meta):
        app_label = 'Core'
        default_manager_name = 'objects'
    
    def get_admin_change_url(self):
        return reverse(
            'admin:{0}_{1}_change'.format(
                "filer",
                "file",
            ),
            args=(self.pk,)
        )

    def get_admin_delete_url(self):
        return reverse(
            'admin:{0}_{1}_delete'.format( "filer","file",),
            args=(self.pk,)
        )

    def save(self, *args, **kwargs):
        folder = str(self.folder)
        meta_information = folder.rsplit('/')
        request_batch = meta_information[1]
        self.batch = Batch.objects.get(batch=int(request_batch))
        self.student = Student.objects.get(student_no=int(self.original_filename.split('.')[0]))
        self.file = compress(self.file, self.original_filename)
        self.has_all_mandatory_data = self._check_validity()
        super().save(*args, **kwargs)

class FilerAdmin(File):

    @classmethod
    def matches_file_type(cls, iname, ifile, mime_type):
        # source: https://www.freeformatter.com/mime-types-list.html
        image_subtypes = ['gif', 'jpeg', 'png', 'x-png', 'svg+xml']
        maintype, subtype = mime_type.split('/')
        return maintype == 'image' and subtype in image_subtypes
