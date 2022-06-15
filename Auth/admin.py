from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from Core.models import *
from import_export.admin import ImportExportModelAdmin
from multiupload.fields import MultiFileField
from django.forms import ModelForm
from import_export.fields import Field
from import_export import resources
from import_export.widgets import ForeignKeyWidget


User = get_user_model()

# class StudentImageResource(resources.ModelResource):
#     class Meta:
#         model = StudentImage
#         fields = ('image',)

class LateEntryResource(resources.ModelResource):
    student_number = Field()
    student_name = Field()
    venue = Field()
    late_count = Field()
    class Meta:
        model = LateEntry
        fields = ('timestamp',)
    
    def dehydrate_student_number(self, instance):
        return instance.student.student_no
    
    def dehydrate_student_name(self, instance):
        return instance.student.name
    
    def dehydrate_venue(self, instance):
        return instance.venue
    
    def dehydrate_late_count(self, instance):
        return instance.student.late_entry.all().count()

class StudentResource(resources.ModelResource):
    branch = Field(
        attribute='branch',
        column_name='branch',
        widget=ForeignKeyWidget(Branch,'name')
        )
    batch = Field(
        attribute='batch',
        column_name='batch',
        widget=ForeignKeyWidget(Batch,'batch')
        )
    
    class Meta:
        model = Student
        fields = ['student_no', 'name']
        export_order = ['student_no', 'name', 'branch', 'batch']
        import_id_fields = ('student_no', 'name', 'branch', 'batch')
    
    def init_instance(self, row=None):
        params = {}
        for key in self.get_import_id_fields():
            field = self.fields[key]
            cleaned_row = field.clean(row)
            params[field.attribute] = field.clean(row)
        student, flag = Student.objects.get_or_create(**params)
        return student
    
    def dehydrate_branch(self, instance):
        print(instance)
        return instance.branch.name
    
    def dehydrate_batch(self, instance):
        return instance.batch.batch

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource

    def delete_model(self, request, obj) -> None:
        obj.student_image.delete()
        return obj.delete()
    
    def delete_queryset(self, request, queryset) -> None:
        queryset.delete()

class LateEntryAdmin(ImportExportModelAdmin):
    resource_class = LateEntryResource
    list_display = ('student', 'venue', 'timestamp')


class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    ordering = ['id']
    list_display = ['email','id', 'name']
    list_filter = ['is_active','is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal Info'), {'fields': ('name',)}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login',)}),
        # ('Group Permissions', {
        #     'classes': ('collapse',),
        #     'fields': ('groups', 'user_permissions', )
        # })
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

    # The forms to add and change user instances
    # add_form = UserAdminCreationForm

admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentImage)
admin.site.register(LateEntry, LateEntryAdmin)
admin.site.register(Batch)
admin.site.register(Branch)
admin.site.register(Venue)
