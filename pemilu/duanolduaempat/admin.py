from django.contrib import admin
from .models import Tps, Chart, Image, Administration


admin.site.register(Tps)
admin.site.register(Chart)
admin.site.register(Image)
admin.site.register(Administration)

# Register your models here.
