from django import forms
from django.forms import fields
from .models import Metrics, RedeemableItem

from leadership.models import User
from django import forms


class AddMetricsForm(forms.ModelForm):
    class Meta:
        model = Metrics
        fields =["metric","value"]
        widgets = {
            'metric':forms.TextInput(attrs={'class':'form_control','id':'metric-input',}),
            'value':forms.NumberInput(attrs={'class':'form_control','id':'metric-value',}),
        }

        
class RewardItemForm(forms.ModelForm):
    class Meta:
        model=RedeemableItem
        fields=["image", "item_name","item_value","quantity"]



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','image')

# Edit User Profile form
