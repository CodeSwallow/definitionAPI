from rest_framework import status
from rest_framework.test import APITestCase
import requests

from dictionary.models import Word, Definition, Synonym, Example
from dictionary.scraper import DictionaryScraper


class WordAPITests(APITestCase):
    url = 'http://localhost:8000/dictionary/definition/'

    @classmethod
    def setUpTestData(cls):
        word = Word.objects.create(word='diverse')
        definition_1 = Definition.objects.create(
            part_of_speech='adjective',
            definition='distinctly dissimilar or unlike',
            word=word
        )
        Synonym.objects.create(word='various', definition=definition_1)
        Synonym.objects.create(word='different', definition=definition_1)
        Example.objects.create(sentence='celebrities as diverse as Bob Hope and Bob Dylan', definition=definition_1)
        definition_2 = Definition.objects.create(
            part_of_speech='adjective',
            definition='many and different',
            word=word
        )
        Synonym.objects.create(word='divers', definition=definition_2)
        Synonym.objects.create(word='different', definition=definition_2)
        Example.objects.create(sentence='a person of diverse talents', definition=definition_2)

    def test_retrieve_existing_word(self):
        url = self.url + 'diverse'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_none_existing_word(self):
        url = self.url + 'profound'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'profound')
        self.assertIn('definitions', response.data)

    def test_retrieve_none_existing_word_adds_word(self):
        url = self.url + 'profound'
        before_get = Word.objects.count()
        response = self.client.get(url, format='json')
        after_get = Word.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('word', response.data)
        self.assertIn('definitions', response.data)
        self.assertEqual(before_get, 1)
        self.assertEqual(after_get, 2)

    def test_retrieve_existing_word_data(self):
        url = self.url + 'diverse'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictEqual(response.data, {
            "id": 1,
            "word": "diverse",
            "definitions": [
                {
                    "id": 1,
                    "part_of_speech": "adjective",
                    "definition": "distinctly dissimilar or unlike",
                    "synonyms": [
                        {
                            "word": "various"
                        },
                        {
                            "word": "different"
                        }
                    ],
                    "antonyms": [],
                    "examples": [
                        {
                            "sentence": "celebrities as diverse as Bob Hope and Bob Dylan"
                        }
                    ]
                },
                {
                    "id": 2,
                    "part_of_speech": "adjective",
                    "definition": "many and different",
                    "synonyms": [
                        {
                            "word": "divers"
                        },
                        {
                            "word": "different"
                        }
                    ],
                    "antonyms": [],
                    "examples": [
                        {
                            "sentence": "a person of diverse talents"
                        }
                    ]
                }
            ]
        })

    def test_retrieve_word_from_plural(self):
        url = self.url + 'animals'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'animal')

    def test_retrieve_plural_does_not_add_to_existing_word(self):
        url = self.url + 'animal'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'animal')
        self.assertEqual(Word.objects.count(), 2)

        url = self.url + 'animals'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['word'], 'animal')
        self.assertEqual(Word.objects.count(), 2)

    def test_retrieve_invalid_word_raises_404(self):
        url = self.url + 'adf invalid 2131'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_invalid_word_does_not_add_to_db(self):
        url = self.url + 'adf invalid 2131'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Word.objects.count(), 1)


class DictionaryScraperTests(APITestCase):
    url = 'https://www.vocabulary.com/dictionary/'
    scraper = DictionaryScraper()

    def test_get_request_response_is_200(self):
        url = self.url + 'animal'
        response = requests.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_word_returns_error(self):
        response = self.scraper.get_word('an 123 df.')
        self.assertIn('error', response)

    def test_scraper_returns_valid_dict(self):
        response = self.scraper.get_word('diverse')
        self.assertIn('word', response)
        self.assertIn('definitions', response)
        self.assertEqual(response['word'], 'diverse')
        self.assertIn('synonyms', response['definitions'][0])
        self.assertIn('antonyms', response['definitions'][0])
        self.assertIn('examples', response['definitions'][0])
