from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
from digital_art.models import DigitalArt
import random
import string
def upload_nature(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload/upload_success.html')  
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload_nature.html', {'form': form})

def generate_unique_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
def upload_success(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    status_message = "Вы успешно загрузили свою картину" if uploaded_file.file.name.endswith('.jpg') else "Вы успешно загрузили свою музыку"

    if request.method == 'POST':
        work_type = uploaded_file.work_type
        theme = uploaded_file.theme
        atmosphere = uploaded_file.atmosphere
        hashtags = uploaded_file.hashtags.split(',')

        if work_type == 'Трек':
            matching_files = UploadedFile.objects.filter(work_type='Обложка', theme=theme, atmosphere=atmosphere)
        else:
            matching_files = UploadedFile.objects.filter(work_type='Трек', theme=theme, atmosphere=atmosphere)

        matching_files = [file for file in matching_files if any(tag in file.hashtags.split(',') for tag in hashtags)]
        if matching_files:
            selected_file = random.choice(matching_files)
            unique_number = generate_unique_number()
            if work_type == 'Трек':
                digital_art = DigitalArt.objects.create(track=uploaded_file, cover=selected_file, unique_number=unique_number)
            else:
                digital_art = DigitalArt.objects.create(cover=uploaded_file, track=selected_file, unique_number=unique_number)
            return redirect('digital_art_detail', unique_number=unique_number)

    return render(request, 'upload/upload_success.html', {
        'status_message': status_message,
        'uploaded_file': uploaded_file,
    })