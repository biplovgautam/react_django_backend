from django import forms
from .widgets import CustomImageWidget

class CustomImageField(forms.FileField):
    widget = CustomImageWidget