from rest_framework import serializers
from .models import School, Classroom, Teacher, Student

# code here
# 1. Serializer สำหรับโรงเรียน
class SchoolSerializer(serializers.ModelSerializer):
    # ฟิลด์พิเศษสำหรับนับจำนวนตามที่โจทย์ต้องการ (read_only คือให้อ่านได้อย่างเดียว ไม่ต้องใส่ตอนสร้างข้อมูล)
    classroom_count = serializers.SerializerMethodField(read_only=True)
    teacher_count = serializers.SerializerMethodField(read_only=True)
    student_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = School
        fields = '__all__' # ดึงฟิลด์ทั้งหมดใน Model มาใช้

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        # นับจำนวนครูที่ไม่ซ้ำกัน ที่สอนในห้องเรียนของโรงเรียนนี้
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        # นับจำนวนนักเรียน ที่อยู่ในห้องเรียนของโรงเรียนนี้
        return Student.objects.filter(classroom__school=obj).count()

# 2. Serializer สำหรับห้องเรียน
class ClassroomSerializer(serializers.ModelSerializer):
    teacher_list = serializers.SerializerMethodField(read_only=True)
    student_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Classroom
        fields = '__all__'

    def get_teacher_list(self, obj):
        return [{"id": t.id, "name": f"{t.first_name} {t.last_name}"} for t in obj.teachers.all()]

    def get_student_list(self, obj):
        return [{"id": s.id, "name": f"{s.first_name} {s.last_name}"} for s in obj.students.all()]

# 3. Serializer สำหรับครู
class TeacherSerializer(serializers.ModelSerializer):
    classroom_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'

    def get_classroom_list(self, obj):
        return [{"id": c.id, "grade": c.grade, "section": c.section} for c in obj.classrooms.all()]

# 4. Serializer สำหรับนักเรียน
class StudentSerializer(serializers.ModelSerializer):
    classroom_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

    def get_classroom_detail(self, obj):
        return {
            "id": obj.classroom.id,
            "grade": obj.classroom.grade,
            "section": obj.classroom.section,
            "school": obj.classroom.school.name
        }