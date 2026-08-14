from django.contrib import admin
from .models import School, Classroom, Teacher, Student

# Register your models here.

# ลงทะเบียนให้ตารางเหล่านี้ไปโชว์ในหน้า Django Admin
admin.site.register(School)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Student)