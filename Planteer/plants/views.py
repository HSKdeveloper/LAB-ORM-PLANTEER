from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Plant
from .models import Contact

# Create your views here.

#create new plant
def create_plant_view(request:HttpRequest):

    if request.method == "POST":

        new_plant = Plant( name = request.POST["name"], about = request.POST["about"], used_for = request.POST["used_for"], image = request.FILES["image"], category = request.POST["category"], is_edible = request.POST["is_edible"], created_at = request.POST["created_at"]  )
        new_plant.save()

        return redirect('main:home_view')

    return render(request, "plants/create-new-plant.html")

#show all plant 
def all_plants_view(request:HttpRequest):

    plants = Plant.objects.all()

    category_filter = request.GET.get('category')
    if category_filter:
        plants = plants.filter(category = category_filter)
    
    is_edible_filter = request.GET.get('is_edible')
    if is_edible_filter:
        if is_edible_filter == 'True':
            plants = plants.filter(is_edible=True)
        elif is_edible_filter == 'False':
            plants = plants.filter(is_edible=False)
    
    context = { "plants" : plants}

    return render(request, "plants/all-plant.html",  context)

#show plant detail
def plant_detail_view(request:HttpRequest, plant_id:int):

    plant = Plant.objects.get(pk=plant_id)
    filter_plant = Plant.objects.all().filter(category = plant.category).exclude(pk=plant.pk)

    return render(request, 'plants/plant-detail.html', {"plant":plant, "filter_plant":filter_plant})

#delete plant
def plant_delete_view(request:HttpRequest, plant_id:int):

    plant = Plant.objects.get(pk=plant_id)
    plant.delete()

    return redirect("main:home_view")

#uodate plant
def plant_update_view (request:HttpRequest, plant_id):
    plant = Plant.objects.get(pk=plant_id)

    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = request.POST["is_edible"]
        plant.created_at = request.POST["created_at"]
        if "image" in request.FILES: plant.image = request.FILES["image"]
        plant.save()
    
        return redirect("plants:plant_detail_view", plant_id=plant.id)
    return render(request,"plants/plant-update.html", {"plant":plant})

#search about plant
def plant_search_view(request:HttpRequest):
    
    if "search" in request.GET:
        plants = Plant.objects.filter(name__contains = request.GET["search"])
    else:
        plants = []
    
    return render(request, "plants/search-plant.html", {"plants":plants})

#contact us page
def contact_us_view(request:HttpRequest):

    if request.method == "POST":

        new_msg = Contact( first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST["email"], message = request.POST["message"],  created_at = request.POST["created_at"]  )
        new_msg.save()

        return redirect('plants:contact_message_view')
    return render(request, "plants/contact-us.html")

#message page
def contact_message_view(request:HttpRequest):

    msg = Contact.objects.all()
    
    return render(request, "plants/message.html",{"msg":msg})