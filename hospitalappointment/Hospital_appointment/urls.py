from django.contrib import admin
from django.urls import include, path
from appointments.views import register_customer, doctor_list, appointment_list, update_medical_record, \
    get_medical_record, add_prescription, check_prescription, show_prescriptions, get_patient, show_patients, \
    add_doctor, doctor_list, add_medicine, show_medicines, create_medical_order, pay, claim, get_medical_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_customer, name = 'register_customer'),#√
    #path('appointments/<int:appointment_id>/', appointment_list, name='appointment_list'),
    path('appointments/', appointment_list, name='appointment_list'),#√
    path('addDoctor/',add_doctor, name='add_doctor'),#√
    path('showDoctors/', doctor_list, name='doctor_list'),#√
    path('updateMedicalRecord/', update_medical_record, name='update_medical_record'),
    path('getMedicalRecord/', get_medical_record, name='get_medical_record'),
    path('getMedicalRecord/<int:patient_id>/', get_medical_record, name='getMedicalRecord'),
    path('addPrescription/<int:patient_id>/', add_prescription, name='add_prescription'),#√
    path('checkPrescription/<int:patient_id>/', check_prescription, name='check_prescription'),#√
    path('showPrescriptions/', show_prescriptions, name='show_prescriptions'),#√
    path('showPatients/',show_patients,name ='show_patients'),#√
    path('getPatient/<int:customer_id>/',get_patient, name='get_patient'),#√
    path('addMedicine/',add_medicine, name='add_medicine'),#√
    path('showMedicines/', show_medicines, name='show_medicines'),#√
    path('updateMedicalOrder/', create_medical_order, name='updateMedicalOrder'),#√
    path('getMedicalOrderByAppointmentId/<int:appointment_id>/', get_medical_order, name='getMedicalOrderByAppointmentId'),#√
    path('pay/', pay, name='pay'),
    path('claim/', claim, name='claim'),
]