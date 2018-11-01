from django.test import TestCase

from api.db_models.inspirehep import User


class AnimalTestCase(TestCase):
    # def setUp(self):
    #     Animal.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        import ipdb; ipdb.set_trace()
        User.objects.create(id=999999)
        #response = self.client.get('/api/literature/123/')
        #print(response)
        assert True