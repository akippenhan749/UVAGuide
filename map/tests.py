from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Event as EventModel


class GoogleAuth(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='admin')
        self.user.set_password('password')
        self.user.save()

    def test_logging_in(self):
        c = Client()
        logged_in = c.login(username='admin', password='password')
        self.assertTrue(logged_in)

    def test_incorrect_password(self):
        self.assertFalse(self.user.check_password('admin'))

    def test_logout(self):
        c = Client()
        c.login(username='admin', password='password')
        self.assertTrue(self.user.is_authenticated)
        c.logout()
        self.assertFalse(self.user.is_anonymous)


class Event(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='admin')
        self.user.set_password('password')
        self.user.save()

    def test_title(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertEqual(e.title, "testTitle")

    def test_location(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertEqual(e.location, "testLocation")

    def test_startTime(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertEqual(e.start_time, datetime(2000, 1, 1, 1, 1))

    def test_endTime(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertEqual(e.end_time, datetime(2021, 10, 31, 4, 30))

    def test_wrongTitle(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertNotEqual(e.title, "The Very Hungry Caterpillar")

    def test_wrongLocation(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertNotEqual(e.location, "Alcatraz")

    def test_wrongStartTime(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertNotEqual(e.start_time, datetime(1111, 11, 11, 11, 11))

    def test_wrongEndTime(self):
        e = EventModel.objects.create(title="testTitle", location="testLocation", start_time=datetime(2000, 1, 1, 1, 1),
                                      end_time=datetime(2021, 10, 31, 4, 30))
        self.assertNotEqual(e.end_time, datetime(1234, 12, 12, 12, 12))


class Routing(TestCase):

    def test_routing_page(self):
        c = Client()
        url = c.get('/route')
        self.assertURLEqual(url,
                            '<HttpResponsePermanentRedirect status_code=301, "text/html; charset=utf-8", url="/route/">')

    def test_routing_redirect(self):
        c = Client()
        url = c.get('/route', {'google_address_a': 'Sprigg Lane, Charlottesville, VA, USA',
                               'google_address_b': 'Rotunda Drive, Charlottesville, VA, USA'}).url
        self.assertURLEqual(url,
                            "/route/?google_address_a=Sprigg+Lane%2C+Charlottesville%2C+VA%2C+USA&google_address_b"
                            "=Rotunda+Drive%2C+Charlottesville%2C+VA%2C+USA")

    def test_directly_to_maps(self):
        c = Client()
        response = c.get('/route/map/').status_code
        self.assertURLEqual(response, 404)

    def testing_wont_redirect(self):
        c = Client()
        response = c.get('/route', {'google_address_a': '+',
                                    'google_address_b': '+'}).status_code
        self.assertURLEqual(response, 301)
