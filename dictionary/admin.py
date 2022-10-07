from django.contrib import admin

from dictionary.models import Word, Definition, Synonym, Antonym, Example

# Register your models here.
admin.site.register(Word)
admin.site.register(Definition)
admin.site.register(Synonym)
admin.site.register(Antonym)
admin.site.register(Example)

