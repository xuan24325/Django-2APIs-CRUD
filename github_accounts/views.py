  
from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def home(request):
    import requests
    import json
    api_request1 = requests.get("https://api.github.com/users?since=100")
    api1 = json.loads(api_request1.content)
    return render(request, 'home.html', {"api":api1})

def user(request):
    if request.method == 'POST':
        import requests
        import json
        user = request.POST['user']
        user_request1 = requests.get("https://api.github.com/users/"+user)
        username = json.loads(user_request1.content)
        return render(request, 'user.html', {'user':user, 'username':username})
    else:
        notfound = "please use Search..."
        return render(request, 'user.html', {'notfound':notfound})



def weather(request):
    cities = City.objects.all() 

    url2 = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=135bc31e44af82a7dc9394b9e5ec68ee'

    err_msg = ''
    message = ''
    message_class = ''


    if request.method == 'POST': 
        form = CityForm(request.POST) 
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count =City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                n = requests.get(url2.format(new_city)).json()
                print(n)
                if n['cod'] == 200:
                    form.save()
                else: 
                    err_msg = 'City does not exits in the database!' 
            else:
                err_msg = 'City already exists in the database!' 
        
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url2.format(city)).json()
        
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)
    
    context = {'weather_data' : weather_data, 
               'form' : form,
               'message' : message,
               'message_class' : message_class
               }

    return render(request, 'weather.html', context) 

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('weather')