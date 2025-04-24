from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from .mongo import crud
import json
from datetime import datetime



def main_page(request):
    # return render(request, "./static/main.html")
    return FileResponse(open('backend/static/main.html', 'rb'))


def scheduling_api(request, dose_id = ""):
    db_object = crud.connect_db()
    if request.method == "GET":
        schedule = db_object.get_pending_doses()
        # json_schedule = json.dumps(schedule)
        # print(json_schedule)
        print("SCHEDULE IS: ")
        print(schedule)
        db_object.close_db()
        return JsonResponse(schedule, safe=False)
    
    elif request.method == "POST":
        if not db_object.get_dose(dose_id):
            return HttpResponse("Dose does not exist", status = 404)
        schedule_time = request.POST.get('Time') # Format - HH:MM
        schedule_date = request.POST.get('Date') # Format - YYYY:MM:DD
        schedule_notes = request.POST.get('Notes')
        schedule_amount = request.POST.get("Amount")
        date_time_str = f'{schedule_date} {schedule_time}'
        schedule_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        db_object.add_insulin_dose(schedule_datetime.strftime('%Y-%m-%d %H:%M'), schedule_amount, schedule_notes)
        db_object.close_db()
        return HttpResponse("Dose Scheduled", status = 201)
    elif request.method == "PUT":
        if not db_object.get_dose(dose_id):
            db_object.close_db()
            return HttpResponse("Dose does not exist", status = 404)
        schedule_dose_id = request.POST.get('Dose_ID')
        schedule_time = request.POST.get('Time') # Format - HH:MM
        schedule_date = request.POST.get('Date') # Format - YYYY:MM:DD
        schedule_status = request.POST.get('Status')
        schedule_notes = request.POST.get('Notes')
        schedule_amount = request.POST.get("Amount")
        date_time_str = f'{schedule_date} {schedule_time}'
        schedule_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        db_object.update_dose(schedule_dose_id, schedule_datetime, schedule_status,schedule_amount, schedule_notes)
        db_object.close_db()
        return HttpResponse("Dose Modified", status = 201)
    
    elif request.method == "DELETE":
        if not db_object.get_dose(dose_id):
            db_object.close_db()
            return HttpResponse("Dose does not exist", status = 404)
        db_object.mark_dose_taken(dose_id)
        db_object.close_db()
        return HttpResponse("Dose Deleted", status = 201)
            
    else:
        db_object.close_db()
        return HttpResponse("Invalid Request", status = 404)
    
