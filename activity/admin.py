from django.contrib import admin
from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(Activity, ActivityAdmin)