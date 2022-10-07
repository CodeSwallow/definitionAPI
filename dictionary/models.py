from django.db import models

# Create your models here.


class Word(models.Model):
    word = models.CharField(max_length=255)

    def __str__(self):
        return self.word


class Definition(models.Model):
    part_of_speech = models.CharField(max_length=255)
    definition = models.CharField(max_length=255)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='definitions')


class Synonym(models.Model):
    word = models.CharField(max_length=255)
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, related_name='synonyms')

    def __str__(self):
        return self.word


class Antonym(models.Model):
    word = models.CharField(max_length=255)
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, related_name='antonyms')

    def __str__(self):
        return self.word


class Example(models.Model):
    sentence = models.CharField(max_length=255)
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, related_name='examples')

    def __str__(self):
        return self.sentence

