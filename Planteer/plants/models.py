from django.db import models

# Create your models here.

class Country(models.Model):

    name = models.CharField(max_length=200, unique= True)
    flag = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

class Plant(models.Model):

    class PlantChoices(models.TextChoices):
        FRUITS = "fruits","Fruits"
        VEGETABLES = "vegetables","Vegtables"
        LEAFY_GREENS = "leafy_greens","Leafy Greens"
        ORNAMENTAL = "ornamental","Ornamental"
        OTHER = "other", "Other"

    name = models.CharField( max_length=1024 )
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/default.png")
    category = models.CharField(max_length=50, choices= PlantChoices.choices)
    is_edible = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now=True)

    countries = models.ManyToManyField( Country )

    def __str__(self):
        return self.name


class Review (models.Model):

    plant = models.ForeignKey( Plant, on_delete=models.CASCADE )

    name = models.CharField(max_length=1024)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    create_at = models.DateTimeField( auto_now_add=True )

    def __str__(self):
        return f"{self.name} on {self.plant.title}"


class Contact(models.Model):

    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
