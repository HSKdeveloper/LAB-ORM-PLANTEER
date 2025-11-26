from django.urls import path
from . import views


app_name = "plants"

urlpatterns = [
    path("new/", views.create_plant_view, name="create_plant_view"),
    path("search/",views.plant_search_view, name="plant_search_view"),
    path("all/",views.all_plants_view, name="all_plants_view"),
    path("detail/<plant_id>/", views.plant_detail_view, name="plant_detail_view"),
    path("delete/<plant_id>/", views.plant_delete_view, name="plant_delete_view"),
    path("update/<plant_id>", views.plant_update_view, name="plant_update_view"),
    path("contact/", views.contact_us_view, name= "contact_us_view"),
    path("message/",views.contact_message_view,name="contact_message_view"),
    path("reviews/add/<plant_id>/", views.add_review_view, name="add_review_view"),
    path("country/<country_name>",views.country_filter_view, name="country_filter_view")
]