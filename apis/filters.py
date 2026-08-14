from django_filters import FilterSet, filters
from .models import School, Classroom, Teacher, Student

# code here
class SchoolFilter(FilterSet):
    # lookup_expr='icontains' คือการค้นหาแบบมีคำบางส่วนก็เจอ และไม่สนใจตัวพิมพ์เล็ก-ใหญ่
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']

class ClassroomFilter(FilterSet):
    school = filters.NumberFilter(field_name='school_id')

    class Meta:
        model = Classroom
        fields = ['school']

class TeacherFilter(FilterSet):
    # distinct=True ป้องกันการดึงข้อมูลครูซ้ำกันกรณีสอนหลายห้อง
    school = filters.NumberFilter(field_name='classrooms__school_id', distinct=True)
    classroom = filters.NumberFilter(field_name='classrooms__id', distinct=True)
    firstname = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    lastname = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(lookup_expr='iexact') # iexact คือตัวอักษรต้องตรงเป๊ะ แต่ไม่สนตัวพิมพ์เล็ก-ใหญ่

    class Meta:
        model = Teacher
        fields = ['school', 'classroom', 'firstname', 'lastname', 'gender']

class StudentFilter(FilterSet):
    school = filters.NumberFilter(field_name='classroom__school_id')
    classroom = filters.NumberFilter(field_name='classroom_id')
    firstname = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    lastname = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Student
        fields = ['school', 'classroom', 'firstname', 'lastname', 'gender']