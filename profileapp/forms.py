from crispy_forms.helper import FormHelper
from django import forms
from django.core.files.images import get_image_dimensions
from django.views.generic import UpdateView

from authapp.models import Person


class UserUpdateInfoForm(forms.ModelForm):
    class Meta:
        model = Person

        fields = (
            'username', 'first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'avatar',
            'bio', 'city', 'birth_date', 'gender', 'relationship')

    def __init__(self, *args, **kwargs):
        super(UserUpdateInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'b-form__input'
            field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ''

            if field_name == 'is_dark_theme':
                field.widget.attrs['class'] = 'а'

            if field_name == 'phone_number':
                field.widget.attrs['placeholder'] = '+7 (123) 456-78-90'

            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'example@gmail.com'

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if not avatar:
            return False

        try:
            w, h = get_image_dimensions(avatar)

            max_width = max_height = 1920
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    f'Пожалуйста, испльзуйте изображения {max_width} x {max_height} пикселов или меньше.')

            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError('Пожалуйста, используйте JPEG, GIF или PNG изображения.')

            if len(avatar) > (2048 * 1024):
                raise forms.ValidationError('Размер файла не может превышать 2 Мб.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            return avatar

        except TypeError:
            raise forms.ValidationError('Пожалуйста, используйте JPEG, GIF или PNG изображения.')

        return avatar
