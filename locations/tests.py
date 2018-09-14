from django.template.defaultfilters import slugify
from django.test import TestCase

from .models import City, State
from .serializers import StateCitySerializer


class CityDetailViewTestCase(TestCase):

    def test_retrieve_city_detail(self):
        state = State.objects.create(name='Rio Grande do Norte')
        city = City.objects.create(name='Natal', state=state)

        response = self.client.get('/api/states/{state_slug}/cities/{city_slug}/'.format(
            state_slug=state.name_slug, city_slug=city.name_slug))
        self.assertEqual(response.status_code, 200)

        expected_payload = StateCitySerializer(instance=city).data
        actual_payload = response.json()

        self.assertDictEqual(actual_payload, expected_payload)

    def test_city_doesnt_exist_returns_404(self):
        state = State.objects.create(name='Rio Grande do Norte')

        response = self.client.get('/api/states/{state_slug}/cities/nonexisting-city/'.format(
            state_slug=state.name_slug))
        self.assertEqual(response.status_code, 404)


class CitiesListViewTestCase(TestCase):
    def setUp(self):
        self.state = State.objects.create(name='São Paulo')
        self.city = City.objects.create(name='Moji-Mirim', state=self.state)

        super().setUp()

    def test_create_new_city(self):
        new_city_data = {
            'name': 'Radugui Fire',
            'state': self.state.name,
        }

        response = self.client.post(path='/api/states/' + self.state.name_slug + '/cities/',
                                    data=new_city_data)
        self.assertEqual(response.status_code, 201)

        persisted_city = City.objects.get(name=new_city_data['name'])
        self.assertEqual(persisted_city.state.id, self.state.id)

    def test_duplicated_city_is_rejected(self):
        existing_city = self.city

        duplicated_city_data = {
            'name': existing_city.name,
            'state': existing_city.state.name,
        }

        response = self.client.post(path='/api/states/' + existing_city.state.name_slug + '/cities/',
                                    data=duplicated_city_data)
        self.assertEqual(response.status_code, 400)

    def test_list_all_cities_of_a_state(self):
        other_city_of_same_state = City.objects.create(name='Campinas', state=self.state)

        noisy_state = State.objects.create(name='Rio de Janeiro')
        noisy_city = City.objects.create(name='Petrópolis', state=noisy_state)

        response = self.client.get('/api/states/' + self.state.name_slug + '/cities/')
        self.assertEqual(response.status_code, 200)

        expected_payload = [
            StateCitySerializer(instance=self.city).data,
            StateCitySerializer(instance=other_city_of_same_state).data
        ]
        actual_payload = response.json()

        self.assertEqual(len(actual_payload), len(expected_payload))
        self.assertListEqual(actual_payload, expected_payload)


class StateModelTestCase(TestCase):
    def setUp(self):
        self.state_name = 'São Paulo'
        self.state = State.objects.create(name=self.state_name)

        super().setUp()

    def test_persistence(self):
        persisted_state = State.objects.get(name=self.state_name)

        self.assertEqual(self.state.id, persisted_state.id)
        self.assertEqual(self.state.name, persisted_state.name)


class CityModelTestCase(TestCase):
    def setUp(self):
        self.state_name = 'São Paulo'
        self.city_name = 'Moji-Mirim'

        self.state = State.objects.create(name=self.state_name)
        self.city = City.objects.create(name=self.city_name, state=self.state)

        super().setUp()

    def test_persistence(self):
        persisted_city = City.objects.get(name=self.city_name)

        self.assertEqual(self.city.id, persisted_city.id)
        self.assertEqual(self.city.name, persisted_city.name)
        self.assertEqual(self.city.state.id, persisted_city.state.id)

    def test_name_slug_is_set_by_default(self):
        city_name_slug = slugify(self.city.name)

        self.assertEqual(self.city.name_slug, city_name_slug)
