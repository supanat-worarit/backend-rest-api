from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apis.models import School, Classroom, Teacher, Student

# Create your tests here.
class BaseAPITest(APITestCase):
    """
    สร้าง Class พื้นฐานสำหรับการ Setup สิ่งที่ต้องใช้ซ้ำๆ ในทุกเทส
    เช่น การจำลอง User สำหรับ Login
    """
    def setUp(self):
        # จำลองการสร้าง User และ Login
        self.user = User.objects.create_user(username='testadmin', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # จำลองข้อมูลพื้นฐานที่ต้องใช้
        self.school = School.objects.create(name="Test School", abbreviation="TS", address="BKK")
        self.classroom = Classroom.objects.create(school=self.school, grade="1", section="A")

class SchoolAPITest(BaseAPITest):
    
    def test_get_school_list(self):
        url = reverse('school-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_school(self):
        url = reverse('school-list')
        data = {"name": "New School", "abbreviation": "NS", "address": "Chiang Mai"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_school(self):
        # การ Update ต้องระบุ ID (pk) ลงไปใน URL ด้วย
        url = reverse('school-detail', kwargs={'pk': self.school.pk})
        data = {"name": "Updated School Name", "abbreviation": "TS", "address": "BKK"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(School.objects.get(pk=self.school.pk).name, "Updated School Name")

    def test_delete_school(self):
        url = reverse('school-detail', kwargs={'pk': self.school.pk})
        response = self.client.delete(url, format='json')
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        self.assertEqual(School.objects.count(), 0)

class ClassroomAPITest(BaseAPITest):

    def test_create_classroom(self):
        url = reverse('classroom-list')
        # ใส่ ID ของ School ที่จำลองไว้ใน BaseAPITest เพื่อเชื่อมความสัมพันธ์
        data = {"school": self.school.id, "grade": "2", "section": "B"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 2)

class TeacherAPITest(BaseAPITest):

    def test_create_teacher(self):
        url = reverse('teacher-list')
        # Many-to-Many ต้องส่งข้อมูลเป็น Array (List) ของ ID
        data = {
            "first_name": "Kru", 
            "last_name": "Yai", 
            "gender": "Male",
            "classrooms": [self.classroom.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 1)

class StudentAPITest(BaseAPITest):

    def test_create_student(self):
        url = reverse('student-list')
        # One-to-Many ส่ง ID ธรรมดา
        data = {
            "first_name": "Dek Ying", 
            "last_name": "Dee", 
            "gender": "Female",
            "classroom": self.classroom.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)