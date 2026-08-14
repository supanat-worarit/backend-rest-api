from django.db import models

# Create your models here.
# 1. ตารางโรงเรียน
class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name

# 2. ตารางห้องเรียน
class Classroom(models.Model):
    # เชื่อมกับ School แบบ 1-to-Many (1 โรงเรียน มีหลายห้องเรียน)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    grade = models.CharField(max_length=50)   # ชั้นปี
    section = models.CharField(max_length=50) # ทับ

    def __str__(self):
        return f"{self.grade}/{self.section} - {self.school.abbreviation}"

# 3. ตารางครู
class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    # เชื่อมกับ Classroom แบบ Many-to-Many (ครู 1 คนมีหลายห้อง, 1 ห้องมีครูหลายคน)
    classrooms = models.ManyToManyField(Classroom, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 4. ตารางนักเรียน
class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)
    # เชื่อมกับ Classroom แบบ 1-to-Many (นักเรียน 1 คนอยู่ได้ห้องเดียว, 1 ห้องมีนักเรียนหลายคน)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"