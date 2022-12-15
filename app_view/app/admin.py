from django.contrib import admin

# Register your models here.
from app.models import PeriodPost, SettingModel, ProgramModel, Categories, Score

admin.site.register(PeriodPost)
admin.site.register(SettingModel)

admin.site.register(ProgramModel)
admin.site.register(Categories)
admin.site.register(Score)