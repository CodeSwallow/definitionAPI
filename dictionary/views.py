from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from dictionary.models import Word, Definition, Synonym, Antonym, Example
from dictionary.serializers import WordSerializer, DefinitionSerializer
from dictionary.scraper import DictionaryScraper

# Create your views here.


class WordUtility:

    @staticmethod
    def add_word(new_word):
        try:
            return Word.objects.get(word=new_word['word']), True
        except Word.DoesNotExist:
            added_word = Word.objects.create(word=new_word['word'])
            for definition in new_word['definitions']:
                added_definition = Definition.objects.create(
                    part_of_speech=definition['part_of_speech'],
                    definition=definition['definition'],
                    word=added_word
                )

                for synonym in definition['synonyms']:
                    Synonym.objects.create(
                        word=synonym,
                        definition=added_definition
                    )

                for antonym in definition['antonyms']:
                    Antonym.objects.create(
                        word=antonym,
                        definition=added_definition
                    )

                for example in definition['examples']:
                    Example.objects.create(
                        sentence=example,
                        definition=added_definition
                    )

            return added_word, False


class WordDetailView(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return Word.objects.get(word=pk)
        except Word.DoesNotExist:
            new_word = DictionaryScraper().get_word(pk)
            if 'error' in new_word:
                raise Http404
            added_word, _ = WordUtility.add_word(new_word)
            return added_word

    def get(self, request, pk):
        word = self.get_object(pk)
        serializer = WordSerializer(word)
        return Response(serializer.data)


class WordViewSet(ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        new_word, existed = WordUtility.add_word(self.request.data)
        if existed:
            return Response({'message': 'Word already exists, nothing added'}, status=status.HTTP_200_OK)
        serializer = WordSerializer(new_word)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def add_definitions(self, request, pk=None):
        instance = self.get_object()
        for definition in request.data:
            added_definition = Definition.objects.create(
                part_of_speech=definition['part_of_speech'],
                definition=definition['definition'],
                word=instance
            )

            for synonym in definition.get('synonyms', []):
                Synonym.objects.create(
                    word=synonym,
                    definition=added_definition
                )

            for antonym in definition.get('antonyms', []):
                Antonym.objects.create(
                    word=antonym,
                    definition=added_definition
                )

            for example in definition.get('examples', []):
                Example.objects.create(
                    sentence=example,
                    definition=added_definition
                )

        serializer = WordSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DefinitionViewSet(ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    permission_classes = [IsAuthenticated]
