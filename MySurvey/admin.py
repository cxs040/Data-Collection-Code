from django.contrib import admin

# Register your models here.
#username: ****, password: *****

from .models import Profile, Product, Question, ProgrammingQuestion, Rating, productResults, programmingResults

myModels = [Profile, Product, Question, ProgrammingQuestion, Rating, productResults,programmingResults]

admin.site.register(myModels)
