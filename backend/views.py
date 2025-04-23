from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from .mongo import crud
import json
from datetime import datetime

def main_page(request):
    # return render(request, "./static/main.html")
    return FileResponse(open('backend/static/main.html', 'rb'))


def scheduling_api(request, dose_id = ""):
    if request.method == "GET":
        schedule = crud.get_pending_doses()
        json_schedule = json.dumps(schedule)
        print(json_schedule)
        return JsonResponse(json_schedule)
    
    elif request.method == "POST":
        if not crud.get_dose(dose_id):
            return HttpResponse("Dose does not exist", status = 404)
        schedule_time = request.POST.get('Time') # Format - HH:MM
        schedule_date = request.POST.get('Date') # Format - YYYY:MM:DD
        schedule_notes = request.POST.get('Notes')
        schedule_amount = request.POST.get("Amount")
        date_time_str = f'{schedule_date} {schedule_time}'
        schedule_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        crud.add_insulin_dose(schedule_datetime.strftime('%Y-%m-%d %H:%M'), schedule_amount, schedule_notes)
        return HttpResponse("Dose Scheduled", status = 201)
    elif request.method == "PUT":
        if not crud.get_dose(dose_id):
            return HttpResponse("Dose does not exist", status = 404)
        schedule_dose_id = request.POST.get('Dose_ID')
        schedule_time = request.POST.get('Time') # Format - HH:MM
        schedule_date = request.POST.get('Date') # Format - YYYY:MM:DD
        schedule_status = request.POST.get('Status')
        schedule_notes = request.POST.get('Notes')
        schedule_amount = request.POST.get("Amount")
        date_time_str = f'{schedule_date} {schedule_time}'
        schedule_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        crud.update_dose(schedule_dose_id, schedule_datetime, schedule_status,schedule_amount, schedule_notes)
        return HttpResponse("Dose Modified", status = 201)
    
    elif request.method == "DELETE":
        if not crud.get_dose(dose_id):
            return HttpResponse("Dose does not exist", status = 404)
        crud.mark_dose_taken(dose_id)
        return HttpResponse("Dose Deleted", status = 201)
            
    else:
        return HttpResponse("Invalid Request", status = 404)
    
    
client.close()
