from django import forms
from plants.models import Plant

#Create the form class
class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = "__all__"
