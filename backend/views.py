from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from .mongo import crud
import json
from datetime import datetime
from bson import json_util
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict



def main_page(request):
    # return render(request, "./static/main.html")
    return FileResponse(open('backend/static/main2.html', 'rb'))

@csrf_exempt
def scheduling_api(request, dose_id = ""):
    db_object = crud.connect_db()
    if request.method == "GET":
        schedule = db_object.get_doses()
        # json_schedule = json.dumps(schedule)
        # print(json_schedule)
        json_data = json_util.dumps(schedule)
        db_object.close_db()
        return JsonResponse(json_data, safe=False)
    
    elif request.method == "POST":
        # schedule_time = request.POST.get('time') # Format - HH:MM
        # schedule_date = request.POST.get('date') # Format - YYYY:MM:DD
        schedule_notes = request.POST.get('scheduled_notes')
        schedule_amount = request.POST.get("scheduled_amount")
        # date_time_str = f'{schedule_date} {schedule_time}'
        # schedule_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        scheduled_time = request.POST.get('scheduled_time')
        scheduled_status = request.POST.get('scheduled_status')
        db_object.add_insulin_dose(scheduled_time, scheduled_status,schedule_amount, schedule_notes)
        db_object.close_db()
        return HttpResponse("Dose Scheduled", status = 201)
    elif request.method == "PUT":
        put_data = QueryDict(request.body).dict()
        schedule_dose_id = put_data.get('dose_id')
        dose_id = schedule_dose_id
        print("PUT")
        print(schedule_dose_id)
        if not db_object.get_dose(dose_id):
            db_object.close_db()
            return HttpResponse("Dose does not exist", status = 404)
        
        schedule_time = put_data.get('time') # Format - HH:MM
        schedule_status = put_data.get('status')
        schedule_notes = put_data.get('notes')
        schedule_amount = put_data.get("amount")
        date_time_str = schedule_time.replace("T", " ").replace("-",":")
        # schedule_datetime = datetime.strptime(date_time_str, '%Y:%m:%d %H:%M')
        db_object.update_dose(schedule_dose_id, date_time_str, schedule_status,schedule_amount, schedule_notes)
        db_object.close_db()
        return HttpResponse("Dose Modified", status = 201)
    
    elif request.method == "DELETE":
        print(request.body)
        json_data = json.loads(request.body)
        dose_id = json_data.get('dose_id')
        print("Deletwe Test")
        print(dose_id)
        if not db_object.get_dose(dose_id):
            db_object.close_db()
            return HttpResponse("Dose does not exist", status = 404)
        db_object.delete_dose(dose_id)
        db_object.close_db()
        return HttpResponse("Dose Deleted", status = 201)
            
    else:
        db_object.close_db()
        return HttpResponse("Invalid Request", status = 404)
    
