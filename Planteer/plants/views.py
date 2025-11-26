from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Plant, Review, Country
from .models import Contact

from .forms import PlantForm

#for pagination
from django.core.paginator import Paginator

#for messages notifications
from django.contrib import messages

# Create your views here.

#create new plant
def create_plant_view(request:HttpRequest):

    #form call
    plant_form = PlantForm()

    countries = Country.objects.all()


    if request.method == "POST":

        plant_form = PlantForm(request.POST)
        if plant_form.is_valid():
            plant_form.save()

            messages.success(request, "Add new plant successfuly", "alert-success")
            return redirect('main:home_view')
        else:
            print("not valid form", plant_form.errors)

        #new_plant = Plant( name = request.POST["name"], about = request.POST["about"], used_for = request.POST["used_for"], image = request.FILES["image"], category = request.POST["category"], is_edible = request.POST["is_edible"])
        #new_plant.save()

        #new_plant.countries.set(request.POST.getlist{"countries"})

        

    return render(request, "plants/create-new-plant.html", {"plant_form":plant_form,"PlantChoices": Plant.PlantChoices.choices,"countries":countries} )

#show all plant 
def all_plants_view(request:HttpRequest):

    plants = Plant.objects.all()
    countries = Country.objects.all()

    #Category_filter
    category_filter = request.GET.get('category')
    if category_filter:
        plants = plants.filter(category = category_filter)
    
    #is_edible filter
    is_edible_filter = request.GET.get('is_edible')
    if is_edible_filter:
        if is_edible_filter == 'True':
            plants = plants.filter(is_edible=True)
        elif is_edible_filter == 'False':
            plants = plants.filter(is_edible=False)
    
    #country filter
    country_filter = request.GET.get('name')
    if country_filter:
        plants = plants.filter(countries__name = country_filter )
        #countries = countries.filter(name = country_filter)
    
    #if "countries.all" in request.GET:
        #countries = Country.objects.filter( countries__id = request.GET[""])

    
    page_number = request.GET.get("page",1)
    paginator = Paginator(plants, 4)
    plants_page = paginator.get_page(page_number )

    
    context = { "plants" : plants_page, "countries":countries}

    return render(request, "plants/all-plant.html",  context)

#show plant detail
def plant_detail_view(request:HttpRequest, plant_id:int):

    #countries  = Country.objects.all()

    plant = Plant.objects.get(pk=plant_id)
    filter_plant = Plant.objects.all().filter(category = plant.category).exclude(pk=plant.pk)

    reviews = Review.objects.filter( plant = plant)

    return render(request, 'plants/plant-detail.html', {"plant":plant, "filter_plant":filter_plant, "reviews":reviews})

#delete plant
def plant_delete_view(request:HttpRequest, plant_id:int):

    try:
        plant = Plant.objects.get(pk=plant_id)
        plant.delete()
        messages.success(request, "Deleted plant successfuly", "alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't delete plant", "alert-danger")


    return redirect("main:home_view")

#update plant
def plant_update_view (request:HttpRequest, plant_id):

    plant = Plant.objects.get(pk=plant_id)

    all_countries = Country.objects.all()

    if request.method == "POST":
        #using PlantForm for update
        plant_form = PlantForm(instance=plant, data= request.POST, files=request.FILES)
        if plant_form.is_valid():
            plant_form.save()
            messages.success(request, "Update plant information successfuly", "alert-success")
        else:
            print(plant_form.errors)


        #plant.name = request.POST["name"]
        #plant.about = request.POST["about"]
        #plant.used_for = request.POST["used_for"]
        #plant.category = request.POST["category"]
        #plant.is_edible = request.POST["is_edible"]
        #if "image" in request.FILES: plant.image = request.FILES["image"]
        #plant.save()
    
        #selected_countries = request.POST.getlist("countries")
        #plant.countries.set(selected_countries)

        return redirect("plants:plant_detail_view", plant_id=plant.id)
    
    return render(request,"plants/plant-update.html", {"plant":plant, "countries":all_countries })

#search about plant
def plant_search_view(request:HttpRequest):

    if "search" in request.GET and len(request.GET ["search"]) >= 1:
        plants = Plant.objects.filter(name__contains = request.GET["search"])

        if "OrderBy" in request.GET and request.GET["OrderBy"] == "name":
            plants = plants.order_by("-name")
        elif "OrderBy" in request.GET and request.GET["OrderBy"] == "release_date":
            plants = plants.order_by("-created_at")
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


#add review
def add_review_view( request:HttpRequest, plant_id:int ):

    if request.method == "POST":
        
        plant_object = Plant.objects.get( pk = plant_id )

        new_review = Review( plant = plant_object,name = request.POST["name"], rating = request.POST["rating"], comment = request.POST["comment"])
        new_review.save()

    return redirect("plants:plant_detail_view", plant_id = plant_id)

#country filter
def country_filter_view( request:HttpRequest, country_name):

    #الطريقة الاولى عند استخدام فيلتر
    #if Country.objects.filter( name = country_name).exists():
     #   plants = Plant.objects.filter( countries__name__in = [country_name]).order_by("-created_at")
    #elif country_name == "all":
     #   plants = Plant.objects.all().order_by("-created_at")
    #else:
     #   plants = []
    
    #الطريقة الثانية عند استخدام فيلتر
    if country_name == "all":
        plants = Plant.objects.all().order_by("-created_at")
    else :
        plants = Plant.objects.filter( countries__name__in = [country_name]).order_by("-created_at")

    return render(request, "plants/country.html", {"plants":plants , "country_name":country_name })
