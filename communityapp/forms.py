from django import forms
from django.core.files.images import get_image_dimensions

from communityapp.models import Community, CommunityNewsItem
from newsapp.forms import CreateNewsForm


class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ("name", "description", "image")

    def __init__(self, *args, **kwargs):
        super(CreateCommunityForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'b-form__input'
            field.widget.attrs["placeholder"] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ""

            if field_name == 'creator':
                field.widget.attrs['class'] = 'd-none'

    def clean_image(self):
        image = self.cleaned_data["image"]

        if not image:
            return False

        try:
            w, h = get_image_dimensions(image)

            max_width = max_height = 1920
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    f'Пожалуйста, испльзуйте изображения {max_width} x {max_height} пикселов или меньше.')

            if len(image) > (2048 * 1024):
                raise forms.ValidationError('Размер файла не может превышать 2 Мб.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            return image

        except TypeError:
            raise forms.ValidationError("Пожалуйста, используйте JPEG, GIF или PNG изображения.")

        return image

    def clean_description(self):
        description = self.cleaned_data['description']
        description = description.replace('\n', '<br>')
        return description


class CreateCommunityNewsForm(CreateNewsForm):
    class Meta:
        model = CommunityNewsItem
        fields = ('text', 'image')

    def __init__(self, *args, **kwargs):
        super(CreateCommunityNewsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'b-form__input'
