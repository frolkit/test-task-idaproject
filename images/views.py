from urllib.parse import urlparse
from django.shortcuts import render, redirect, get_object_or_404
from sorl.thumbnail import get_thumbnail

from .models import Image
from .forms import ImageCreate, ImageEdit


def index(request):
    queryset = Image.objects.all()
    return render(request, 'index.html', {'queryset': queryset})


def image_create(request):
    form = ImageCreate(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            image_link = form.cleaned_data['image_link']
            image_file = form.cleaned_data['image_file']
            if image_link:
                file_name = urlparse(image_link).path.split('/')[-1]
            else:
                file_name = image_file.name
            instance = Image()
            instance.image.save(file_name, image_file)
            return redirect("image_edit", id=instance.id)
    return render(request, 'image_create.html', {'form': form})


def resize_image(image, width=None, height=None):
    '''
       support format:
       1920
       x1080
       1920x1080
    '''
    geometry = ''
    if width:
        geometry += str(width)
    if height:
        geometry += 'x' + str(height)
    return get_thumbnail(image, geometry, crop='center')


def image_edit(request, id):
    instance = get_object_or_404(Image, id=id)
    image = instance.image
    if instance.width or instance.height:
        image = resize_image(image=image,
                             width=instance.width,
                             height=instance.height)
    form = ImageEdit(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            return redirect("image_edit", id=instance.id)
    return render(request, 'image_edit.html', {'form': form,
                                               'image': image})
