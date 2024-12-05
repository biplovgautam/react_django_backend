from django import forms
from .models import ProductImage
from .fields import CustomImageField

class ProductImageForm(forms.ModelForm):
    image_file = CustomImageField(required=False)

    class Meta:
        model = ProductImage
        fields = ['product', 'alt_text', 'image_file']

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_file = self.cleaned_data.get('image_file')
        if uploaded_file:
            instance.image = uploaded_file.read()
        if commit:
            instance.save()
        return instance