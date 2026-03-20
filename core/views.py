from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, request
from django.db.models import Count
from openpyxl import Workbook

from .models import Student, Faculty, ExtraField, StudentExtraData


# ======================
# LOGIN
# ======================
from django.contrib import messages

def login_view(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.groups.filter(name="Admin").exists():
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


# ======================
# ADMIN DASHBOARD
# ======================
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Student, Faculty


@login_required
def admin_dashboard(request):

    total_students = Student.objects.count()

    total_boys = Student.objects.filter(
        gender__iexact="male"
    ).count()

    total_girls = Student.objects.filter(
        gender__iexact="female"
    ).count()

    total_departments = Student.objects.values('department').distinct().count()

    teaching_faculty = Faculty.objects.filter(
    staff_type__icontains="teach"
    ).count()

    non_teaching = Faculty.objects.filter(
    staff_type__icontains="non"
    ).count()

    context = {
        'total_students': total_students,
        'total_boys': total_boys,
        'total_girls': total_girls,
        'total_departments': total_departments,
        'teaching_faculty': teaching_faculty,
        'non_teaching': non_teaching
    }

    return render(request, 'admin_dashboard.html', context)


# ======================
# FACULTY LIST (ADMIN ONLY)
# ======================
@login_required
def faculty_list(request):

    if not request.user.groups.filter(name="Admin").exists():
        return HttpResponseForbidden()

    faculty = Faculty.objects.all()

    q = request.GET.get('q')
    dept = request.GET.get('dept')

    if q:
        faculty = faculty.filter(
            Q(name__icontains=q) |
            Q(department__icontains=q) |
            Q(designation__icontains=q)
        )

    if dept:
        faculty = faculty.filter(department=dept)

    return render(request, 'faculty_list.html', {
        'faculty': faculty
    })


# ======================
# FACULTY VIEW
# ======================
@login_required
def faculty_view(request, id):
    if not request.user.groups.filter(name="Admin").exists():
        return HttpResponseForbidden()

    faculty = get_object_or_404(Faculty, id=id)

    return render(request, 'faculty_view.html', {
        'faculty': faculty
    })


# ======================
# FACULTY EDIT
# ======================
@login_required
def faculty_edit(request, id):
    if not request.user.groups.filter(name="Admin").exists():
        return HttpResponseForbidden()

    faculty = get_object_or_404(Faculty, id=id)

    if request.method == "POST":
        faculty.name = request.POST.get('name')
        faculty.department = request.POST.get('department')
        faculty.designation = request.POST.get('designation')
        faculty.save()

        messages.success(request, "Faculty updated successfully")

        return redirect('faculty_list')

    return render(request, 'faculty_edit.html', {
        'faculty': faculty
    })

@login_required
def add_faculty(request):
    if not request.user.groups.filter(name="Admin").exists():
        return HttpResponseForbidden()

    if request.method == "POST":
        Faculty.objects.create(
            name=request.POST.get('name'),
            department=request.POST.get('department'),
            designation=request.POST.get('designation'),
            staff_type=request.POST.get('staff_type')
        )
        messages.success(request, "Faculty added successfully")
        return redirect('faculty_list')

    return render(request, 'add_faculty.html')


# ======================
# STUDENT DASHBOARD
# ======================
@login_required
@login_required
def student_dashboard(request):
    student = Student.objects.filter(user=request.user).first()

    if not student:
        return redirect('admin_dashboard')  # prevent crash

    return render(request, 'student_dashboard.html', {'student': student})


# ======================
# ADD STUDENT
# ======================
from django.contrib.auth.models import User
from django.contrib import messages
@login_required


@login_required
def add_student(request):
    if request.method == "POST":
        roll_no = request.POST.get('roll_no')

        if User.objects.filter(username=roll_no).exists():
            messages.error(request, "Student already exists")
            return redirect('add_student')

        # ✅ CREATE USER
        user = User.objects.create_user(
            username=roll_no,
            password="1234"
        )

        # 🔥 DEPARTMENT LOGIC
        department = request.POST.get('department').strip().title()
        

        # ✅ CREATE STUDENT
        Student.objects.create(
            user=user,
            name=request.POST.get('name'),
            roll_no=roll_no,
            department=department,
            admission_year=request.POST.get('admission_year'),
            course=request.POST.get('course')
        )

        messages.success(request, "Student added successfully")

        return redirect('student_list')

    return render(request, 'add_student.html')



# ======================
# STUDENT DETAIL (VIEW)
# ======================
@login_required
def student_detail(request, id):
    student = Student.objects.get(id=id)

    fields = []

    for field in student._meta.fields:
        name = field.name

        # skip unwanted
        if name in ['id', 'user']:
            continue

        value = getattr(student, name)

        if value:
            fields.append({
                'label': name.replace('_', ' ').title(),
                'value': value
            })

    return render(request, 'student_detail.html', {
        'student': student,
        'fields': fields
    })


# ======================
# STUDENT EDIT
# ======================
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def student_edit(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        print(request.POST)

        # BASIC
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.department = request.POST.get('department')
        student.course = request.POST.get('course')

        # DATE FIX
        dob = request.POST.get('dob')
        student.dob = dob if dob else None

        student.gender = request.POST.get('gender')
        student.blood_group = request.POST.get('blood_group')
        student.religion = request.POST.get('religion')
        student.category = request.POST.get('category')
        student.aadhaar = request.POST.get('aadhaar')

        student.physically_challenged = request.POST.get('physically_challenged') == "True"

        # CONTACT
        student.phone = request.POST.get('phone')
        student.email = request.POST.get('email')
        student.permanent_address = request.POST.get('permanent_address')

        # FAMILY
        student.father_name = request.POST.get('father_name')
        student.mother_name = request.POST.get('mother_name')
        student.father_occupation = request.POST.get('father_occupation')
        student.mother_occupation = request.POST.get('mother_occupation')
        student.father_phone = request.POST.get('father_phone')
        student.mother_phone = request.POST.get('mother_phone')

        # 🔥 SAFE NUMBER CONVERSION
        def to_int(val):
            try:
                return int(val)
            except:
                return None

        def to_float(val):
            try:
                return float(val)
            except:
                return None

        student.tenth_year = to_int(request.POST.get('tenth_year'))
        student.tenth_percentage = to_float(request.POST.get('tenth_percentage'))
        student.twelfth_year = to_int(request.POST.get('twelfth_year'))
        student.twelfth_percentage = to_float(request.POST.get('twelfth_percentage'))

        # ACADEMIC
        student.course = request.POST.get('course')
        student.batch = request.POST.get('batch')
        student.hosteller = request.POST.get('hosteller') == "True"

        student.save()

        messages.success(request, "Student details updated successfully")

        return redirect('student_full_details', id=student.id)

    return render(request, 'student_edit.html', {'student': student})


# ======================
# CHANGE PASSWORD
# ======================
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # ❌ Validation
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('change_password')

        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect('change_password')

        # ✅ Save
        user = request.user
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully")

        return redirect('student_dashboard')

    return render(request, 'change_password.html')


# ======================
# EXPORT EXCEL
# ======================
from openpyxl import Workbook
from django.http import HttpResponse

def export_excel(request):
    if request.method == "POST":

        selected_fields = request.POST.getlist('fields')
        data_type = request.POST.get('type')
        department = request.POST.get('department')

        wb = Workbook()
        ws = wb.active

        ws.append(selected_fields)

        if data_type == "faculty":
            queryset = Faculty.objects.all()
        else:
            queryset = Student.objects.all()

        # ✅ FIXED FILTER
        if department and department != "All":
            queryset = queryset.filter(department=department)

        data = queryset.values(*selected_fields)

        for row in data:
            ws.append([row.get(field, "") for field in selected_fields])

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=data.xlsx'

        wb.save(response)
        return response

from django.shortcuts import render
from .models import Student
from .models import Student, Faculty
@login_required

def export_page(request):

    student_fields = [f.name for f in Student._meta.fields]
    faculty_fields = [f.name for f in Faculty._meta.fields]

    return render(request, 'export_excel.html', {
        'student_fields': student_fields,
        'faculty_fields': faculty_fields
    })

from .models import StudentExtraData

from django.http import HttpResponseForbidden

@login_required
def student_full_details(request, id):
    student = Student.objects.get(id=id)

    # 🔥 SECURITY CHECK
    if not request.user.groups.filter(name="Admin").exists():
        if student.user != request.user:
            return HttpResponseForbidden()

    extra_data = StudentExtraData.objects.filter(student=student)

    return render(request, 'student_full_details.html', {
        'student': student,
        'extra_data': extra_data
    })

from django.db.models import Q

@login_required
def student_list(request):

    q = request.GET.get('q', '').strip()
    dept = request.GET.get('dept', '').strip()
    gender = request.GET.get('gender', '').strip()
    course_type = request.GET.get('type', '').strip()

    students = Student.objects.all()

    # 🔍 SEARCH
    if q:
        students = students.filter(
            Q(name__icontains=q) |
            Q(roll_no__icontains=q) |
            Q(department__icontains=q) |
            Q(user__email__icontains=q)
        )

    # 🏫 DEPARTMENT
    if dept:
        students = students.filter(department__iexact=dept)

    # 🚻 GENDER
    if gender:
        students = students.filter(gender__iexact=gender)

    # 🎓 COURSE
    if course_type:
        students = students.filter(course__iexact=course_type)

    return render(request, 'student_list.html', {
        'students': students
    })


from django.db.models import Count, Q

@login_required
def programmes(request):

    departments = Student.objects.values('department').annotate(
        total_students=Count('id'),
        boys=Count('id', filter=Q(gender__icontains='m')),
        girls=Count('id', filter=Q(gender__icontains='f'))
    )

    # Add faculty count manually
    dept_data = []

    for d in departments:
        faculty_count = Faculty.objects.filter(
            department=d['department']
        ).count()

        dept_data.append({
            'name': d['department'],
            'total_students': d['total_students'],
            'boys': d['boys'],
            'girls': d['girls'],
            'faculty': faculty_count
        })

    return render(request, 'programmes.html', {
        'departments': dept_data
    })
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import get_object_or_404, redirect

def delete_student(request, id):
    student = Student.objects.get(id=id)

    # delete linked user FIRST
    if student.user:
        student.user.delete()

    student.delete()

    return redirect('student_list')

def delete_faculty(request, id):
    faculty = Faculty.objects.get(id=id)

    # delete linked user FIRST (if exists)
    if hasattr(faculty, 'user') and faculty.user:
        faculty.user.delete()

    faculty.delete()

    return redirect('faculty_list')

def digilocker(request):
    return render(request, 'digilocker.html')

from .models import Student

@login_required
def export_view(request):

    student_fields = [f.name for f in Student._meta.fields]
    faculty_fields = [f.name for f in Faculty._meta.fields]

    departments = Student.objects.exclude(
        department__isnull=True
    ).exclude(
        department__exact=''
    ).values_list('department', flat=True).distinct()

    return render(request, 'export.html', {
        'student_fields': student_fields,
        'faculty_fields': faculty_fields,
        'departments': departments
    })
