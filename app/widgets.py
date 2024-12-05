from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import base64

class CustomImageWidget(ClearableFileInput):
    template_name = 'custom_image_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        if value and isinstance(value, bytes):
            # Convert binary data to base64 string
            base64_image = base64.b64encode(value).decode('utf-8')
            context['widget'].update({
                'value': base64_image,
                'is_image': True,
            })
        else:
            context['widget']['is_image'] = False
        return mark_safe(render_to_string(self.template_name, context))