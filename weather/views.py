from django.shortcuts import render,redirect
from .models import City
from .forms import add_weather_form
import requests

# Create your views here.
def home_view(request,*args, **kwargs):
    err = ''
    message = ''
    message_class = ''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=db0826790bd3408951f454f513a0f98b'
    cities = City.objects.all()

    if request.method == 'POST':
        form = add_weather_form(request.POST or None)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            current_count = City.objects.filter(name = city_name).count()
            if current_count==0:
                r = requests.get(url.format(city_name)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err = 'city does not exist , try a different city :)'    
            else:
                err = 'City already exists in the current page'
        if err:
            message = err
            message_class = 'is-danger'
        else:
            message = 'City Added Successfully'
            message_class = 'is-success'                
    form = add_weather_form()    
    weather_data = []
    
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city':city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
        context = {
            'weather_data':weather_data,
            'form':form,
            'message':message,
            'message_class':message_class
            
        }
    return render(request,'layout.html', context)

def delete_view(request,delete_name):
    City.objects.get(name = delete_name).delete()
    return redirect('home')    