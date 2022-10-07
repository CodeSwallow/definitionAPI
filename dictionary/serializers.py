from rest_framework import serializers

from dictionary.models import Word, Definition, Synonym, Antonym, Example


class SynonymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Synonym
        fields = ['word']


class AntonymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Antonym
        fields = ['word']


class ExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Example
        fields = ['sentence']


class DefinitionSerializer(serializers.ModelSerializer):
    synonyms = SynonymSerializer(many=True, read_only=True)
    antonyms = AntonymSerializer(many=True, read_only=True)
    examples = ExampleSerializer(many=True, read_only=True)

    class Meta:
        model = Definition
        fields = ['id', 'part_of_speech', 'definition', 'synonyms', 'antonyms', 'examples']


class WordSerializer(serializers.ModelSerializer):
    definitions = DefinitionSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = ['id', 'word', 'definitions']
