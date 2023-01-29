from django.shortcuts import render
from calendar import monthcalendar
import datetime
from .models import Attendance

# Create your views here.
def attendance(request):

    today = datetime.date.today()
    year = today.year
    month = today.month
    cal = monthcalendar(year, 2)

    if request.method == "POST":
        res = request.POST
        print(month)
        ec = request.user
        for att in res:
            dt = str(att) + '-' + str(month) + '-' + str(year)
            print(ec, dt, res[att])
            # attendance = Attendance()
            # attendance.EmpCode = ec
            # attendance.Date = dt
            # attendance.Status = res[att]
            # attendance.save(force_update=True)

    return render(request, "attendance.html", {'cal':cal})