from django import forms
from django.core.files.images import get_image_dimensions

from newsapp.models import NewsItem


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ('text', 'image')

    def __init__(self, *args, **kwargs):
        super(CreateNewsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ''

    def clean_user(self, request):
        user = request.user
        return user

    def clean_image(self):
        image = self.cleaned_data['image']

        if not image:
            return False

        try:
            w, h = get_image_dimensions(image)

            max_width = max_height = 1920
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    f'Пожалуйста, испльзуйте изображения {max_width} x {max_height} пикселов или меньше.')

            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError('Пожалуйста, используйте JPEG, GIF или PNG изображения.')

            if len(image) > (2048 * 1024):
                raise forms.ValidationError('Размер файла не может превышать 2 Мб.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            return image

        except TypeError:
            raise forms.ValidationError('Пожалуйста, используйте JPEG, GIF или PNG изображения.')

        return image

    def clean_text(self):
        text = self.cleaned_data['text']
        text = text.replace('\n', '<br>')
        return text
