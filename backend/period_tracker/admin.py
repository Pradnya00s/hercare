from django.contrib import admin
from .models import Cycle, SymptomLog, LifestyleLog

admin.site.register(Cycle)
admin.site.register(SymptomLog)
admin.site.register(LifestyleLog)