from django.shortcuts import render,redirect
from datetime import date,datetime,timedelta
from .forms import AppointmentForm
from .models import Appointment
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from administrator.models import Doctor,DoctorScheduleTime
from administrator.models import DoctorLeave
from utils.sendmessage import send_whatsapp_message
from django.conf import settings


User = get_user_model()


# Create your views here.

def book_appointment(request):

    form = AppointmentForm()
    success = False

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        # 🔥 RE-INJECT SLOT CHOICES (CRITICAL)
        selected_time = request.POST.get("time")

        if selected_time:
            form.fields["time"].choices = [(selected_time, selected_time)]

        if form.is_valid():

            # 🚫 BLOCK PAST DATE
            selected_date = form.cleaned_data["date"]

            if selected_date < date.today():
                form.add_error("date", "Past date not allowed")

            else:
                try:
                    # 🔥 CREATE APPOINTMENT
                    appointment=Appointment.objects.create(
                        first_name=form.cleaned_data["first_name"],
                        last_name=form.cleaned_data["last_name"],
                        phone=form.cleaned_data["phone"],
                        email=form.cleaned_data["email"],
                        specialization=form.cleaned_data["specialization"],
                        doctor=form.cleaned_data["doctor"],
                        date=form.cleaned_data["date"],
                        time=form.cleaned_data["time"],
                    )

                      # ================= 🔥 SEND WHATSAPP HERE =================
                    message = f"""
                              New Appointment Booking

                              Patient: {appointment.first_name}
                              Doctor: {appointment.doctor}
                              Date: {appointment.date}
                              Time: {appointment.time}
                             """
                    
                    send_whatsapp_message(settings.ADMIN_WHATSAPP_NUMBER,message)

                    # =========================================================

                    form = AppointmentForm()
                    success = True

                except Exception:
                    form.add_error(None, "This slot is already booked")

    return render(request, "booking/book.html", {
        "form": form,
        "success": success
    })

def load_doctors(request):

    specialization_id = request.GET.get("specialization")

    doctors = Doctor.objects.filter(
        specialization_id=specialization_id
    ).values("id", "user__first_name")

    data = list(doctors)

    return JsonResponse(data, safe=False)



def load_slots(request):

    doctor_id = request.GET.get("doctor")
    selected_date = request.GET.get("date")

    if not doctor_id or not selected_date:
        return JsonResponse([], safe=False)

    # 🔥 Convert to date object
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

    # ================= 🔥 STEP 1: CHECK LEAVE =================
    leaves = DoctorLeave.objects.filter(
        doctor_id=doctor_id,
        date=selected_date_obj
    )

    # ❌ FULL DAY LEAVE
    if leaves.filter(is_full_day=True).exists():
        return JsonResponse([], safe=False)

    # 🔥 Get day of week
    day_of_week = selected_date_obj.weekday()

    # ================= GENERATE SLOTS =================
    schedules = DoctorScheduleTime.objects.filter(
        schedule__doctor_id=doctor_id,
        day_of_week=day_of_week,
        is_active=True,
        schedule__is_active=True
    )

    all_slots = []

    for sch in schedules:

        start = datetime.combine(selected_date_obj, sch.start_time)
        end = datetime.combine(selected_date_obj, sch.end_time)

        while start < end:

            all_slots.append(start.strftime("%H:%M"))

            start += timedelta(minutes=sch.slot_duration)

    # 🔥 Remove duplicates + sort
    all_slots = sorted(set(all_slots))

    # ================= KEEP YOUR EXISTING LOGIC =================

    # 🔥 GET BOOKED SLOTS
    booked = Appointment.objects.filter(
        doctor_id=doctor_id,
        date=selected_date_obj
    ).values_list("time", flat=True)

    booked_slots = [t.strftime("%H:%M") for t in booked]

    # 🔥 REMOVE BOOKED
    available_slots = [
        slot for slot in all_slots if slot not in booked_slots
    ]

    # 🔥 REMOVE PAST TIME (ONLY TODAY)
    if selected_date_obj == date.today():

        current_time = datetime.now().time()

        filtered_slots = []

        for slot in available_slots:
            slot_time = datetime.strptime(slot, "%H:%M").time()

            if slot_time > current_time:
                filtered_slots.append(slot)

        available_slots = filtered_slots

    # ================= 🔥 STEP 2: APPLY PARTIAL LEAVE =================
    for leave in leaves:

        if not leave.is_full_day and leave.start_time and leave.end_time:

            filtered_slots = []

            for slot in available_slots:

                slot_time = datetime.strptime(slot, "%H:%M").time()

                # ❌ REMOVE slots inside leave time
                if not (leave.start_time <= slot_time < leave.end_time):
                    filtered_slots.append(slot)

            available_slots = filtered_slots

    return JsonResponse(available_slots, safe=False)