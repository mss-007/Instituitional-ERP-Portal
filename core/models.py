from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    admission_year = models.IntegerField()

    # BASIC
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)

    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    # EXTRA DETAILS
    religion = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    physically_challenged = models.BooleanField(default=False)

    aadhaar = models.CharField(max_length=20, blank=True, null=True)

    permanent_address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)

    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)

    father_phone = models.CharField(max_length=15, blank=True, null=True)
    mother_phone = models.CharField(max_length=15, blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)

    tenth_year = models.IntegerField(null=True, blank=True)
    tenth_percentage = models.FloatField(null=True, blank=True)

    twelfth_year = models.IntegerField(null=True, blank=True)
    twelfth_percentage = models.FloatField(null=True, blank=True)

    # 🎓 PROGRAMME TYPE (THIS WAS MISSING BEFORE)
    COURSE_CHOICES = [
        ('UG', 'UG'),
        ('PG', 'PG'),
        ('Research', 'Research'),
    ]

    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        default='UG',
        blank=True,
        null=True
    )

    batch = models.CharField(max_length=50, blank=True, null=True)
    hosteller = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Faculty(models.Model):

    STAFF_TYPE_CHOICES = [
        ('teaching', 'Teaching'),
        ('non_teaching', 'Non Teaching'),
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    staff_type = models.CharField(
        max_length=20,
        choices=STAFF_TYPE_CHOICES,
        default='teaching'
    )

    def __str__(self):
        return self.name


class ExtraField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudentExtraData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field = models.ForeignKey(ExtraField, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.field.name}"