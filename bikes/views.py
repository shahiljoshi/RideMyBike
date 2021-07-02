from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import Station, Bike, Rental, User as BikeUser ,Payment
from datetime import datetime
# Create your views here.

plans = ['HOURLY', 'DAILY', 'WEEKLY']
global plan_choosed
global family_rental


def home(request, *args, **kwargs):
    if request.user.is_authenticated:
        current_rentals = {'rentals': request.user.rental_set.all().filter(end_station__isnull=True)}
        return render(request, 'bikes/home.html', context=current_rentals)
    else:
        return render(request, 'bikes/home.html')


def about(request):
    return render(request, 'bikes/about.html')


def stations(request):
    if request.method == 'POST':
        print(request.POST)

        if 'return_station' in request.POST:
            return_bike(request, request.POST['rental_id'], request.POST['station_id'])
            return redirect('rental_detail', rental_id=request.POST['rental_id'])

        if 'station_select' in request.POST:
            return redirect('station_detail', station_id=request.POST['station_id'])

        if 'bike_return' in request.POST:
            s = {'stations': Station.objects.all()}
            s.update(request.POST)
            print(s)
            s['rental_id'] = int(s['rental_id'][0])
            return render(request, 'bikes/stations.html', context=s)
            pass
        return reverse('station_detail', kwargs={'station_id': request.POST['s_id']})
    return render(request, 'bikes/stations.html', context={'stations': Station.objects.all()})


def station_detail(request, station_id):
    if request.method == 'POST':
        global plan_choosed
        plan_choosed = request.POST.get("plan")
        print(request.POST.get("plan"))
        print(request.POST.getlist('b_id'))
        s = get_object_or_404(Bike, pk=request.POST['b_id'])
        out = rent_bike(request, station_id, request.POST.getlist('b_id'), request.user)
        return home(request, alerts=[out])
    s = get_object_or_404(Station, pk=station_id)
    # total_bikes = s.bike_set.all().filter(available=True).filter(working=True).count()
    # print(total_bikes)
    return render(request,
                  'bikes/station_details.html',
                  context={'station': s,
                           'bikes': s.bike_set.all().filter(available=True).filter(working=True),
                           'plans': plans})


def rent_bike(request, station_id, bike_id, user):
    if user.balance > 500:
        print("plan ypu choosed", plan_choosed)
        station = Station.objects.select_for_update().get(pk=station_id)
        if len(user.rental_set.all().filter(end_station__isnull=True)) >= 3:
            messages.error(request, "you already rented 3 bikes")
        r = Rental(user=user, start_date=datetime.now(), start_station=station, plan=plan_choosed)
        r.save()
        for i in bike_id:
            bikes = Bike.objects.filter(pk=int(i))
            Bike.objects.filter(pk=int(i)).update(available=False)
            r.bike.add(i)
            print(bikes)
        print(r)
        messages.success(request, "bike rented successfully")
    else:
        messages.warning(request, "please deposite at least 500 ")
        return render(request, 'bikes/recharge.html')


def return_bike(request, rental_id, station_id):
    Rental.objects.select_for_update()
    Bike.objects.select_for_update()
    BikeUser.objects.select_for_update()
    rental = Rental.objects.get(pk=rental_id)
    end_station = Station.objects.get(pk=station_id)
    rental.bike.all().update(available=True)
    rental.bike.all().update(station=end_station)
    rental.end_station = end_station
    rental.end_date = datetime.now()
    print(type(rental.plan))
    global family_rental
    if rental.plan == 'HOURLY':
        charge = 10*rental.bike.count()
    elif rental.plan == 'DAILY':
        charge = 50*rental.bike.count()
    else:
        charge = 150*rental.bike.count()
    # charge = 50

    if rental.bike.count() >= 3:
       charge -= charge*30/100
       family_rental = True
    else:
        family_rental =False
    rental.cost = charge
    rental.user.balance -= charge
    rental.user.save()
    rental.save()
    p = Payment(rental=rental, status=True)
    p.save()
    messages.success(request, f"Bike returned successfully. Charged user for the rental Rs{charge}.")
    return redirect('rental_detail', rental_id=rental.id)


def rental_detail(request, rental_id):
    rental = Rental.objects.get(pk=rental_id)
    if request.user != rental.user:
        messages.warning(request, 'You cannot see this rental, sorry.')
        return render(request,
                      'bikes/home.html',
                      {'rentals': request.user.rental_set.all().filter(end_station__isnull=True)})
    return render(request,
                  'bikes/rental_detail.html',
                  {'rental': rental})


def recharge(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        if int(request.POST['amount']) < 0:
            messages.warning(request, 'Negative amount')
            return render(request, 'bikes/recharge.html', context={})
        amount = int(request.POST['amount'])
        request.user.balance += int(request.POST['amount'])
        request.user.save()
        messages.success(request, f'Amount Rs.{amount} Added To Your Wallet')
    return render(request, 'bikes/recharge.html')