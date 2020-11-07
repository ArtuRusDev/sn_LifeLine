from django import forms
from newsapp.models import NewsItem


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        # fields = ('user', 'text',)
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CreateNewsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize

            field.help_text = ''
            field.label = ''

    def clean_user(self, request):
        user = request.user
        return user
