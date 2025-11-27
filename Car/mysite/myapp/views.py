from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ShuttleRequest, Car, Driver
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def login_view(request):
    if request.method == "POST":
        user = authenticate(request,
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "myapp/login.html", {"error": "ล็อกอินผิดพลาด"})

    return render(request, "myapp/login.html")


@login_required
def dashboard(request):
    today = timezone.now().date()
    qs = ShuttleRequest.objects.filter(start_time__date=today).order_by('start_time')
    return render(request, "myapp/dashboard.html", {"queue_list": qs})


@login_required
def history(request):
    qs = ShuttleRequest.objects.all()
    
    # กรองตามชื่อ
    search_name = request.GET.get('name', '')
    if search_name:
        qs = qs.filter(user_name__icontains=search_name)
    
    # กรองตามวันที่เริ่มต้น
    date_from = request.GET.get('date_from', '')
    if date_from:
        qs = qs.filter(start_time__date__gte=date_from)
    
    # กรองตามวันที่สิ้นสุด
    date_to = request.GET.get('date_to', '')
    if date_to:
        qs = qs.filter(start_time__date__lte=date_to)
    
    qs = qs.order_by("-start_time")
    
    return render(request, "myapp/history.html", {
        "history": qs,
        "search_name": search_name,
        "date_from": date_from,
        "date_to": date_to,
    })


@login_required
def queue_create(request):
    if request.method == "POST":
        shuttle = ShuttleRequest(
            user_name=request.POST["user_name"],
            line_user_id=request.POST.get("line_user_id", ""),
            pickup_location=request.POST["pickup_location"],
            dropoff_location=request.POST["dropoff_location"],
            start_time=request.POST["start_time"],
            status=request.POST.get("status", "pending")
        )
        
        car_id = request.POST.get("car")
        driver_id = request.POST.get("driver")
        
        if car_id:
            shuttle.car_id = car_id
        if driver_id:
            shuttle.driver_id = driver_id
            
        shuttle.save()
        return redirect("dashboard")
    
    cars = Car.objects.filter(active=True)
    drivers = Driver.objects.all()
    return render(request, "myapp/queue_form.html", {
        "cars": cars,
        "drivers": drivers,
        "action": "เพิ่มคิว"
    })


@login_required
def queue_edit(request, pk):
    shuttle = get_object_or_404(ShuttleRequest, pk=pk)
    
    if request.method == "POST":
        shuttle.user_name = request.POST["user_name"]
        shuttle.line_user_id = request.POST.get("line_user_id", "")
        shuttle.pickup_location = request.POST["pickup_location"]
        shuttle.dropoff_location = request.POST["dropoff_location"]
        shuttle.start_time = request.POST["start_time"]
        shuttle.status = request.POST.get("status", "pending")
        
        car_id = request.POST.get("car")
        driver_id = request.POST.get("driver")
        
        shuttle.car_id = car_id if car_id else None
        shuttle.driver_id = driver_id if driver_id else None
        
        shuttle.save()
        return redirect("dashboard")
    
    cars = Car.objects.filter(active=True)
    drivers = Driver.objects.all()
    return render(request, "myapp/queue_form.html", {
        "shuttle": shuttle,
        "cars": cars,
        "drivers": drivers,
        "action": "แก้ไขคิว"
    })


@login_required
def queue_delete(request, pk):
    shuttle = get_object_or_404(ShuttleRequest, pk=pk)
    
    if request.method == "POST":
        shuttle.delete()
        return redirect("dashboard")
    
    return render(request, "myapp/queue_confirm_delete.html", {"shuttle": shuttle})


@login_required
def car_list(request):
    cars = Car.objects.all().order_by('-active', 'license_plate')
    return render(request, "myapp/car_list.html", {"cars": cars})


@login_required
def car_create(request):
    if request.method == "POST":
        car = Car(
            license_plate=request.POST["license_plate"],
            name=request.POST.get("name", ""),
            color=request.POST.get("color", ""),
            active=request.POST.get("active") == "on"
        )
        car.save()
        return redirect("car_list")
    return render(request, "myapp/car_form.html", {"action": "เพิ่มรถ"})


@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        car.license_plate = request.POST["license_plate"]
        car.name = request.POST.get("name", "")
        car.color = request.POST.get("color", "")
        car.active = request.POST.get("active") == "on"
        car.save()
        return redirect("car_list")
    return render(request, "myapp/car_form.html", {"car": car, "action": "แก้ไขรถ"})


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        car.delete()
        return redirect("car_list")
    return render(request, "myapp/car_confirm_delete.html", {"car": car})


@login_required
def driver_list(request):
    drivers = Driver.objects.all().order_by('name')
    return render(request, "myapp/driver_list.html", {"drivers": drivers})


@login_required
def driver_create(request):
    if request.method == "POST":
        driver = Driver(
            name=request.POST["name"],
            phone=request.POST.get("phone", "")
        )
        driver.save()
        return redirect("driver_list")
    return render(request, "myapp/driver_form.html", {"action": "เพิ่มคนขับ"})


@login_required
def driver_edit(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        driver.name = request.POST["name"]
        driver.phone = request.POST.get("phone", "")
        driver.save()
        return redirect("driver_list")
    return render(request, "myapp/driver_form.html", {"driver": driver, "action": "แก้ไขคนขับ"})


@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == "POST":
        driver.delete()
        return redirect("driver_list")
    return render(request, "myapp/driver_confirm_delete.html", {"driver": driver})


def logout_view(request):
    logout(request)
    return redirect("login")

@csrf_exempt
def api_queue_create(request):
    """สร้างคิวใหม่จาก LINE / n8n"""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body.decode("utf-8"))

    req = ShuttleRequest.objects.create(
        user_name=data.get("user_name", "LINE USER"),
        pickup_location=data.get("pickup_location", "ไม่ระบุ"),
        dropoff_location=data.get("dropoff_location", "ไม่ระบุ"),
        start_time=data.get("start_time") or timezone.now(),
        status="pending",
        line_user_id=data.get("line_user_id"),
    )

    return JsonResponse({"status": "ok", "queue_id": req.id})
    

def api_queue_today(request):
    """ดึงคิววันนี้ (กรองตาม line_user_id ได้)"""
    line_user_id = request.GET.get("line_user_id")
    today = timezone.localdate()

    qs = ShuttleRequest.objects.filter(start_time__date=today).order_by("start_time")
    if line_user_id:
        qs = qs.filter(line_user_id=line_user_id)

    items = []
    for q in qs:
        items.append({
            "id": q.id,
            "user_name": q.user_name,
            "pickup_location": q.pickup_location,
            "dropoff_location": q.dropoff_location,
            "start_time": q.start_time.isoformat(),
            "status": q.status,
        })

    return JsonResponse({"status": "ok", "items": items})


@csrf_exempt
def api_queue_cancel(request):
    """ยกเลิกคิวล่าสุดของ user ในสถานะ pending"""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    line_user_id = data.get("line_user_id")

    if not line_user_id:
        return JsonResponse({"error": "line_user_id is required"}, status=400)

    obj = (
        ShuttleRequest.objects
        .filter(line_user_id=line_user_id, status="pending")
        .order_by("-start_time")
        .first()
    )

    if not obj:
        return JsonResponse({"status": "not_found"}, status=404)

    obj.status = "cancelled"
    obj.save()

    return JsonResponse({"status": "ok", "queue_id": obj.id})

