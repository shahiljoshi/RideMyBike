from builtins import bin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from .models import Station, Bike, Rental, User as BikeUser, Payment
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import time
# Create your views here.


plans = ['HOURLY', 'DAILY', 'WEEKLY']

global plan_choosed
global family_rental


def home(request, *args, **kwargs):
    """

    :param request:
    :param args:
    :param kwargs:
    :return:
    home function shows the current rented bikes of user by the rental_set function for multiple data
    """
    if request.user.is_authenticated:
        current_rentals = {'rentals': request.user.rental_set.all().filter(end_station__isnull=True)}
        print(current_rentals['rentals'])
        end_time = 0
        for i in current_rentals['rentals']:
            end_time = (i.start_date+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
            print(i.plan)
        print(end_time)
        print(timezone.now())
        print(datetime.now() + timedelta(hours=1))
        context = {'rentals': request.user.rental_set.all().filter(end_station__isnull=True),'time':end_time}
        return render(request, 'bikes/home.html', context=context)
    else:
        return render(request, 'bikes/home.html')


def about(request):
    """

    :param request:
    :return:
    about function shows the information about the initiative
    """
    return render(request, 'bikes/about.html')


def faq(request):
    """

    :param request:
    :return:
    faq function will help the customers by answering the question  generally the chatbot by dialogflow
    """
    return render(request, 'bikes/faq.html')


@login_required()
def stations(request):
    """

    :param request:
    :return:
    station function shows the available station and customer chooses nearest station including start station to end station
    """
    if request.method == 'POST':
        print(request.POST)

        if 'return_station' in request.POST:
            return_bike(request, request.POST['rental_id'], request.POST['station_id'])
            return redirect('rental_detail', rental_id=request.POST['rental_id'])

        if 'selected_station' in request.POST:
            return redirect('station_detail', station_id=request.POST['station_id'])

        if 'return_bike' in request.POST:
            station = {'stations': Station.objects.all()}
            station.update(request.POST)
            print(station)
            station['rental_id'] = int(station['rental_id'][0])
            return render(request, 'bikes/stations.html', context=station)
            pass
        return reverse('station_detail', kwargs={'station_id': request.POST['station_id']})
    return render(request, 'bikes/stations.html', context={'stations': Station.objects.all()})


@login_required()
def station_detail(request, station_id):
    """

    :param request:
    :param station_id:
    :return:
    station detail function shows the available bikes at choosed station and plans to choose and also dynamic map by google map
    """
    if request.method == 'POST':
        global plan_choosed
        plan_choosed = request.POST.get("plan")
        print(request.POST.get("plan"))
        print(request.POST.getlist('bike_id'))
        station = get_object_or_404(Bike, pk=request.POST['bike_id'])
        rented_bikes = rent_bike(request, station_id, request.POST.getlist('bike_id'), request.user)
        return home(request, current_rentals=rented_bikes)
    station = get_object_or_404(Station, pk=station_id)
    # total_bikes = s.bike_set.all().filter(available=True).filter(working=True).count()
    # print(total_bikes)
    return render(request,
                  'bikes/station_details.html',
                  context={'station': station,
                           'bikes': station.bike_set.all().filter(available=True).filter(working=True),
                           'plans': plans})


@login_required()
def rent_bike(request, station_id, bike_id, user):
    """

    :param request:
    :param station_id:
    :param bike_id:
    :param user:
    :return:
    rent bike function used after choosing the bikes and plan for renting the bike for user
    transaction atomic is the feature that lock the transaction of the user(rental half transaction)
    """
    with transaction.atomic():
        if user.balance > 500:
            # Rental.objects.filter()
            print("plan you choosed", plan_choosed)
            station = Station.objects.select_for_update().get(pk=station_id)
            r = Rental(user=user, start_station=station, plan=plan_choosed)
            r.save()
            end_time = datetime.now() + timedelta(hours=1)
            print("end time from func",end_time)
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


@login_required()
def return_bike(request, rental_id, station_id):
    """

    :param request:
    :param rental_id:
    :param station_id:
    :return:

    return bike function is use for returning the bike if the customer return the bike late then he has to pay penalty accordingly
    here the transaction atomic use for completing the half transaction that in rent bike and here completes the full entry
    here the final payment cut from the user wallet
    """
    with transaction.atomic():
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
            print(datetime.now().strftime('%Y-%m-%d %H:%M'))
            # Rental.objects.filter(start_date__hour=)
            start=Rental.objects.get(id=rental.id).start_date
            print(start)
            print((rental.start_date + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'))
            # print(rental.start_date)
            if datetime.now().strftime('%Y-%m-%d %H:%M') <= (rental.start_date + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M') :
            # if rental.end_date <= (rental.start_date + timedelta(hours=1)):
                charge = 10*rental.bike.count()
            else:
                messages.warning(request,"Penalty Of Rs.100")
                charge = (10*rental.bike.count())+100

        elif rental.plan == 'DAILY':
            if datetime.now().strftime('%Y-%m-%d %H:%M') <= (rental.start_date + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M'):

                charge = 50*rental.bike.count()
            else:
                messages.warning(request,"Penalty Of Rs.150")
                charge = (50*rental.bike.count())+150

        else:
            if datetime.now().strftime('%Y-%m-%d %H:%M') <= (rental.start_date + timedelta(hours=168)).strftime('%Y-%m-%d %H:%M'):
                charge = 150*rental.bike.count()
            else:
                messages.warning(request,"Penalty Of Rs.250")
                charge = (50*rental.bike.count())+250

        # charge = 50

        if rental.bike.count() >= 3:
           charge -= charge*30/100
           family_rental = True
        else:
            family_rental = False
        rental.cost = charge
        rental.user.balance -= charge
        rental.user.save()
        rental.save()
        p = Payment(rental=rental, status=True)
        p.save()
        messages.success(request, f"Bike returned successfully. Charged user for the rental Rs{charge}.")
    return redirect('rental_detail', rental_id=rental.id)


@login_required()
def rental_detail(request, rental_id):
    """

    :param request:
    :param rental_id:
    :return:
     rental detail function generates the information of rental and have option to generate the pdf of the bill
    """
    rental = Rental.objects.get(pk=rental_id)
    if rental.plan == 'HOURLY':
       cost= rental.bike.count()*10
       family = (cost*30)/100

    if rental.plan == 'DAILY':
       cost= rental.bike.count()*50
       family = (cost*30)/100

    if rental.plan == 'WEEKLY':
       cost= rental.bike.count()*150
       family = (cost*30)/100

    if request.user != rental.user:
        messages.warning(request, 'You cannot see this rental, sorry.')
        return render(request,
                      'bikes/home.html',
                      {'rentals': request.user.rental_set.all().filter(end_station__isnull=True)})
    return render(request,
                  'bikes/rental_detail.html',
                  {'rental': rental,'family':family,'discount_rate':cost})


@login_required()
def recharge(request):
    """

    :param request:
    :return:
    recharge function use for the user wallet balance
    """
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        if int(request.POST['amount']) < 0:
            messages.warning(request, 'Negative amount')
            return render(request, 'bikes/recharge.html', context={})
        if int(request.POST['amount']) > 1000:
            messages.warning(request, 'Amount Greater Than 1000 Not allowed')
            return render(request, 'bikes/recharge.html', context={})
        amount = int(request.POST['amount'])
        request.user.balance += int(request.POST['amount'])
        request.user.save()
        messages.success(request, f'Amount Rs.{amount} Added To Your Wallet')
    return render(request, 'bikes/recharge.html')


def contactView(request):
    """

    :param request:
    :return:
    contact view function for user to contact support from our team
    """
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            # print(name,email,message)

            try:
                send_mail(name, message, email, [email, "shahiljoshi98@gmail.com"])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

    return render(request, "bikes/contact.html")


@login_required()
def user_rentals(request):
    """

    :param request:
    :return:
    user_rentals function show the past rentals of user that logged in
    """
    if not request.user.is_authenticated:
        return redirect('home')
    rentals = request.user.rental_set.all().filter(end_station__isnull=False).order_by('-end_date')[:5]
    if request.method == 'POST':
        print(request.POST)
        if "show_all_rentals" in request.POST:
            rentals = request.user.rental_set.all().filter(end_station__isnull=False).order_by('-end_date')
            return render(request, 'bikes/rentals.html', context={'rentals': rentals})

    return render(request, 'bikes/rentals.html', context={'rentals': rentals})
