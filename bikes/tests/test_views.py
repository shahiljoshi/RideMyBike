from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.messages import get_messages
from bikes.models import Bike, Station, Rental, Payment
from users.models import User
import datetime


class TestViews(TestCase):
    """
        setup user
    """
    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="shahil1@gmail.com",
                                             address="address",
                                             phone_number="9228110541",
                                             password="pass@123"
                                             )
        self.user1 = User.objects.create_user(username="user12",
                                              email="shahil12@gmail.com",
                                              address="address",
                                              phone_number="9228110542",
                                              balance=1000,
                                              password="pass@123"
                                              )

    """
     Home Page Get And Post
    """
    def test_should_show_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/home.html')
        print(response.context)

    def test_should_show_home_page_data(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        response = self.client.post(reverse('home'),current_rentals={'rentals': self.user.rental_set.all().filter(end_station__isnull=True)})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/home.html')
        print(response.context)

    """
        About Page Get
    """

    def test_should_show_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/about.html')
    """
        Faq Get
    """

    def test_should_show_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/faq.html')

    """
        Contact Page Post
    """
    def test_should_show_contact_page(self):
        response = self.client.post(reverse('contact'),
                                    data={'name': 'shahil',
                                          'email': 'shahiljoshi9827@gmail.com',
                                          'message': 'hello'}
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/contact.html')
    """
        Recharge Get And Post
    """
    def test_should_show_recharge_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        response = self.client.get(reverse('recharge'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/recharge.html')

    def test_should_show_recharge_amount_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        amount = 1000
        response = self.client.post(reverse('recharge'),
                                    data={'amount': 1000}
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/recharge.html')
        storage = list(get_messages(response.wsgi_request))
        print(storage)
        for i in storage:
            print(i)
        self.assertIn(f'Amount Rs.{amount} Added To Your Wallet',
                              list(map(lambda x: x.message, storage)))

    def test_should_show_recharge_amount_up_page(self):
        #amount greater than 1000
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        amount = 1500
        response = self.client.post(reverse('recharge'),data={'amount':1500})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/recharge.html')
        storage = list(get_messages(response.wsgi_request))
        print(storage)
        for i in storage:
            print(i)
        self.assertIn('Amount Greater Than 1000 Not allowed',
                              list(map(lambda x: x.message, storage)))

    def test_should_show_recharge_amount_negative_page(self):
        #amount Negative
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        response = self.client.post(reverse('recharge'),data={'amount':-10})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/recharge.html')
        storage = list(get_messages(response.wsgi_request))
        print(storage)
        for i in storage:
            print(i)
        self.assertIn('Negative amount',
                              list(map(lambda x: x.message, storage)))

    """
        Station Get and Post
    """
    def test_should_show_station_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        response = self.client.get(reverse('stations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/stations.html')
        print(response.context)

    def test_should_show_station_page_station_selected(self):
        #selected station from options
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        response = self.client.post(reverse('stations'),
                                    data={'selected_station': '',
                                          'station_id': station.id}
                                    )
        self.assertEqual(response.status_code,302 )
        # self.assertTemplateUsed(response, 'bikes/stations.html')
        print(response.context)

    def test_should_show_station_page_station_return(self):
        #selecting return station
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        rental=Rental.objects.create(user=self.user, start_station=station, plan='HOURLY')
        response = self.client.post(reverse('stations'),
                                    data={'return_station': '',
                                          'station_id': station.id,
                                          'rental_id': rental.id}
                                    )
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'bikes/stations.html')
        print(response.context)
    """
        Station Detail Get
    """
    def test_should_show_station_detail_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        response = self.client.get(reverse('station_detail', args=(station.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/station_details.html')
        print(response.context)
        storage = list(get_messages(response.wsgi_request))
        print(storage)
        for i in storage:
            print(i)
    """
        Rent A Bike After Selecting All Details
    """

    def test_should_show_station_detail_page_rent(self):

        self.client.post(reverse('login'), {
            'email': self.user1.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        bike = Bike.objects.create()
        bike1 = Bike.objects.create()
        bike2 = Bike.objects.create()
        response = self.client.post(reverse('station_detail',
                                            args=(station.id,)),
                                    data={'plan': 'HOURLY',
                                          'bike_id': [bike.id,bike1.id,bike2.id]}
                                    )
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'bikes/station_details.html')
        print(response.context)

    def test_should_show_station_detail_page_not_rent(self):
        # user = User.objects.create_user(username="user1", email="shahil1@gmail.com", address="address",
        #                                 phone_number="9228110541", password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        bike = Bike.objects.create()
        bike1 = Bike.objects.create()
        bike2 = Bike.objects.create()
        response = self.client.post(reverse('station_detail',
                                            args=(station.id,)),
                                    data={'plan': 'HOURLY',
                                          'bike_id': [bike.id,bike1.id,bike2.id]}
                                    )
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'bikes/station_details.html')
        print(response.context)
    """
        Returning Bike After Completion
    """
    def test_should_show_station_page_bike_return(self):
        # user = User.objects.create_user(username="user1", email="shahil1@gmail.com", address="address",
        #                                 phone_number="9228110541", password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        station = Station.objects.create(address="Naranpura")
        rental = Rental.objects.create(user=self.user, start_station=station, plan='HOURLY')
        response = self.client.post(reverse('stations'),
                                    data={'return_bike': '',
                                          'station_id': station.id,
                                          'rental_id': rental.id}
                                    )
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'bikes/stations.html')
        print(response.context)
    """
        Show Returned Bike Rental Details After The Ride Ends
    """
    def test_should_show_rental_detail_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        bike = Bike.objects.create()
        start_station = Station.objects.create(address="Naranpura")
        end_station = Station.objects.create(address="Gurukul")
        rental = Rental.objects.create(user=self.user,start_date=datetime.datetime.now(),end_date=datetime.datetime.now(),start_station=start_station,end_station=end_station,cost=50,plan='HOURLY')
        rental.bike.add(bike.id)
        response = self.client.get(reverse('rental_detail', args=(rental.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/rental_detail.html')
        print(response.context)
        storage = list(get_messages(response.wsgi_request))
        print(storage)
        for i in storage:
            print(i)

    """
        Rental Get And Post Show Users Past Rentals
    """
    def test_should_show_rental_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        response = self.client.get(reverse('rentals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/rentals.html')
        print(response.context)

    def test_should_show_all_rental_page(self):
        # user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        self.client.post(reverse('login'), {
            'email': self.user.email,
            'password': 'pass@123'
        })
        response = self.client.post(reverse('rentals'), data={'show_all_rentals': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bikes/rentals.html')
        print(response.context)

