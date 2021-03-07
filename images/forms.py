from PIL import Image as TestImage
from urllib.request import urlopen
from io import BytesIO
from django import forms
from django.forms import ModelForm, ValidationError

from .models import Image


class ImageEdit(ModelForm):
    class Meta:
        model = Image
        fields = ['width', 'height']


class ImageCreate(forms.Form):
    image_link = forms.URLField(label='Ссылка', required=False)
    image_file = forms.ImageField(label='Файл', required=False)

    def get_image_from_link(self, link):
        image_file_content = BytesIO(urlopen(link).read())
        try:
            TestImage.open(image_file_content)
        except Exception:
            error_message = (
                'По указанному адресу не получилось найти изображение, попробуйте ввести другой адрес.' # noqa
            )
            raise ValidationError(error_message)
        return image_file_content

    def clean(self):
        cleaned_data = super().clean()
        image_link = cleaned_data.get("image_link")
        image_file = cleaned_data.get("image_file")
        if image_link and image_file:
            raise ValidationError("Укажите только один вариант загрузки.")
        elif not image_link and not image_file:
            raise ValidationError("Не указан вариант загрузки.")
        elif image_link:
            image_file = self.get_image_from_link(image_link)
            cleaned_data['image_file'] = image_file
        return cleaned_data
