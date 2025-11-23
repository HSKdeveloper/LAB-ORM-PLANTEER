from django.contrib import admin
from .models import Plant, Review, Contact, Country

# Register your models here.
class PlantAdmin (admin.ModelAdmin):

    list_display = ("name", "category", "is_edible")
    list_filter = ("category",)

class ReviewAdmin (admin.ModelAdmin):

    list_display = ("name", "plant", "rating")
    list_filter = ("plant" , "rating")

admin.site.register(Plant, PlantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Contact)
admin.site.register(Country)