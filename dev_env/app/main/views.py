import sqlite3
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from .models import Patient, Patient_Record, Patient_Record_Doctor
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage


from .forms import RegistrationForm
from django.shortcuts import redirect

from django.http import JsonResponse

def index(request):
    data_list = []
    if request.user.is_authenticated:
        conn = sqlite3.connect("Z:/summerSoursework22/summerСoursework/telegramBotMedical-/mydatabase.db")
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM patient')

        rows = cursor.fetchall()
        
        for row in rows:

            patient = Patient.objects.get_or_create(
                
                patientName=row[1],
                patientPassportDetails=row[2],
                patientGender=row[6],
                patientAge=row[8],
                patientPhone=row[5]
            )
            


        for row in rows:
            patient_data = {
                'patient_id': row[0],
                'name': row[1],  
                'passport': row[2],  
                'sex': row[6], 
                'age': row[8],
                'telephone': row[5] 
            }
            data_list.append(patient_data)

        conn.close()
    
    return render(request, 'main/index.html', {'data_list': data_list})


def user_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user=user)
            return redirect("main:index")
        else:
            error_message = 'Неверное имя пользователя или пароль'
            return render(request, 'main/login.html', {'error_message': error_message})
    return render(request, 'main/login.html')
    


def user_logout(request):
    logout(request)
    return redirect("main:login")


def electronic_medical_card(request):
    # if request.method == 'POST':
    #     print(1234)
    #     patient_id = request.POST.get('patient_id')
    #     patient = get_object_or_404(Patient, id=patient_id)
    #     record = get_object_or_404(Patient_Record, patient=patient)

    #     # Обновление каждой записи врача
    #     for record_doctor in Patient_Record_Doctor.objects.filter(patient_record=record):
    #         doctor_report_key = 'doctor_report_file_{}'.format(record_doctor.id)
    #         doctor_report = request.FILES.get(doctor_report_key, None)
    #         brief_doctor_report = request.POST.get('briefDoctorReport_{}'.format(record_doctor.id), '').strip()
    #         pathology = request.POST.get('pathology_{}'.format(record_doctor.id), '').strip()

    #         if not doctor_report and not brief_doctor_report:
    #             record_doctor.delete()
    #         else:
    #             if doctor_report:
    #                 record_doctor.doctorReportWord = doctor_report
    #             record_doctor.briefDoctorReport = brief_doctor_report
    #             record_doctor.pathology = pathology
    #             record_doctor.save()

    #     return redirect('main:electronic_medical_card', patient_id=patient_id)

    if request.method == 'GET':
        user_groups = request.user.groups.values_list('name', flat=True)
        roles = {
            'is_user': 'User',
            'is_therapist': 'Therapist',
            'is_radiologist': 'Radiologist',
            'is_gynecologist': 'Gynecologist',
            'is_ophthalmologist': 'Ophthalmologist',
            'is_cardiologist': 'Cardiologist',
            'is_procedural_nurse': 'Procedural_nurse',
            'is_mammologist': 'Mammologist',
            'is_urologist': 'Urologist',
        }

        context = {role: role_name in user_groups for role, role_name in roles.items()}

        patient_id = request.GET.get('patient_id')
        patient = get_object_or_404(Patient, id=patient_id)

        current_user = request.user
        doctor_profile = get_object_or_404(Profile, user_id=current_user.id)

        record, created = Patient_Record.objects.get_or_create(patient=patient)

        patient_record_doctor, prd_created = Patient_Record_Doctor.objects.get_or_create(
            patient_record=record,
            doctor=doctor_profile,
            defaults={
                'pathology': '',
                'briefDoctorReport': '',
                'doctorReportWord': None,
            }
        )

        patient_record_doctor.doctor = doctor_profile
        patient_record_doctor.save()

        patient_records_doctors = Patient_Record_Doctor.objects.filter(patient_record=record)

        # Обработка для удаления записей врачей, если поля пустые
        for record_doctor in patient_records_doctors:
            brief_doctor_report = record_doctor.briefDoctorReport.strip()
            pathology = record_doctor.pathology.strip()

            if not record_doctor.doctorReportWord and not brief_doctor_report:
                record_doctor.delete()

        # Обновление списка после возможного удаления
        patient_records_doctors = Patient_Record_Doctor.objects.filter(patient_record=record)

        context.update({
            'doctorReportWord': patient_record_doctor.doctorReportWord,
            'pathology': patient_record_doctor.pathology,
            'brief_doctor_report': patient_record_doctor.briefDoctorReport,
            'patient_id': patient_id,
            'passport': request.GET.get('passport'),
            'name': request.GET.get('name'),
            'sex': request.GET.get('sex'),
            'age': request.GET.get('age'),
            'telephone': request.GET.get('telephone'),
            'patient_records_doctors': patient_records_doctors,
            'current_user': current_user,
        })

        return render(request, 'main/electronicMedicalCard.html', context) 
    

def questionnaire(request):
    passport = request.GET.get('passport')

    if request.user.is_authenticated:
        conn = sqlite3.connect("Z:/summerSoursework22/summerСoursework/telegramBotMedical-/mydatabase.db")
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM patient WHERE passportDetails = ?', (passport,))
        row = cursor.fetchone()

        if row:
            patient_data = {
                "user_id":row[0],
                "user_name":row[1],
                "user_passport":row[2],
                "user_city":row[3],
                "user_address":row[4],
                "user_telephone":row[5],
                "user_gender":row[6],
                "user_datetime":row[7],
                "user_age":row[8],
                "user_height":row[9],
                "user_weight":row[10],
                "user_briefDescriptionComplaintsDate":row[11],
                "user_allergicReactions":row[12],
                "user_hyperallergicReactionstonicDisease":row[13],
                "user_takeHyperallergicMedications":row[14], 
                "user_cardiacIschemia":row[15],
                "user_cerebrovascularDisease":row[16],
                "user_chronicDisease":row[17],
                "user_tuberculosis":row[18],
                "user_diabetes":row[19], 
                "user_takeMedications":row[20],
                "user_stomachDiseases":row[21],
                "user_chronicKidneyDisease":row[22],
                "user_malignantNeoplasm":row[23],
                "user_whichMalignantNeoplasm":row[24],
                "user_elevatedСholesterol":row[25],
                "user_drugsElevatedСholesterol":row[26],
                "user_myocardium":row[27],
                "user_stroke":row[28],
                "user_myocardialInfarction":row[29],
                "user_Relatives":row[30],
                "user_chestDiscomfort":row[31], 
                "user_ifChestDiscomfort":row[32], 
                "user_termWeakness":row[33],
                "user_numbness":row[34],
                "user_visionLoss":row[35],
                "user_cough":row[36],
                "user_wheezing":row[37],
                "user_hemoptysis":row[38],
                "user_upperAbdomen":row[39],
                "user_poop":row[40],
                "user_lostWeight":row[41],
                "user_holes":row[42],
                "user_bleeding":row[43],
                "user_smoke":row[44],
                "user_howManySmoke":row[45], 
                "user_walking":row[46],
                "user_diet":row[47],
                "user_addSomeSalt":row[48],
                "user_narcotic":row[49],
                "user_quantityAlcoholic":row[50],
                "user_youUseAlcoholic":row[51],
                "user_totalPoints":row[52],
                "user_countPoints":row[53],
                "user_otherComplaints":row[54],
            }

        conn.close()

        context = {
            'patient_data': patient_data
        }

        return render(request, 'main/questionnaire.html', context)
    else:
        return redirect('main:login')
    
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Profile
from django.contrib.auth.models import Group

def distribute_users_to_groups(user_profile):
    if user_profile.doctor == 'is_radiologist':
        group_name = 'Radiologist'

    elif user_profile.doctor == 'is_gynecologist':
        group_name = 'Gynecologist'

    elif user_profile.doctor == 'is_ophthalmologist':
        group_name = 'Ophthalmologist'

    elif user_profile.doctor == 'is_cardiologist':
        group_name = 'Cardiologist'

    elif user_profile.doctor == 'is_procedural_nurse':
        group_name = 'Procedural_nurse'

    elif user_profile.doctor == 'is_mammologist':
        group_name = 'Mammologist'

    elif user_profile.doctor == 'is_urologist':
        group_name = 'Urologist'

    elif user_profile.doctor == 'is_therapist':
        group_name = 'Therapist'

    else:
        group_name = 'Error'
    
    group, _ = Group.objects.get_or_create(name=group_name)
    
    user_profile.user.groups.add(group)

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            user_profile = Profile.objects.get(user=user)
            
            distribute_users_to_groups(user_profile)
            
            return redirect('main:login')
    else:
        form = RegistrationForm()
    return render(request, 'main/registration.html', {'form': form})



from django.http import HttpResponse
from .models import Profile, Patient, Patient_Record

def save_changes(request):
    if request.method == 'POST':
        user = request.user

        if not user.is_authenticated:
            return HttpResponse(status=403)

        patient_id = request.POST.get('patient_id')
        passport = request.POST.get('passport')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        telephone = request.POST.get('telephone')
        doctor_report = request.POST.get('doctor_report')
        pathology = request.POST.get('pathology')

        
        if not pathology:
            return JsonResponse({'error': 'Выберите наличие патологии'}, status=400)

        
        patient = Patient.objects.filter(id=patient_id).first()
        if not patient:
            return HttpResponse(status=404)

        
        profile = Profile.objects.filter(user=user).first()
        if not profile:
            return HttpResponse(status=404)
        
        record, created = Patient_Record.objects.get_or_create(patient=patient)

        patient_record_doctor, created = Patient_Record_Doctor.objects.get_or_create(
            patient_record=record,
            doctor=profile,
            defaults={
                'pathology': '',
                'briefDoctorReport': '',
                'doctorReportWord': None
            }
        )

        patient_record_doctor.patientName = name
        patient_record_doctor.pathology = pathology
        patient_record_doctor.briefDoctorReport = doctor_report

        # Если загружен файл с отчетом врача, сохраняем его
        if 'doctor_report_file' in request.FILES:
            doctor_report_file = request.FILES['doctor_report_file']
            # Сохранение файла
            file_path = default_storage.save(doctor_report_file.name, doctor_report_file)
            # Присвоение пути к файлу записи врача
            patient_record_doctor.doctorReportWord = file_path

        # Сохранение изменений в записи врача
        patient_record_doctor.save()

        

        
        return render(request, 'main/success.html', {
            'patient_id': patient_id,
            'passport': passport,
            'name': name,
            'sex': sex,
            'age': age,
            'telephone': telephone
        })

    return HttpResponse(status=405)


