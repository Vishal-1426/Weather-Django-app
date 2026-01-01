from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):

    # -------- CITY INPUT --------
    if request.method == "POST" and request.POST.get("city"):
        city = request.POST.get("city")
    else:
        city = "indore"

    # -------- WEATHER API --------
    WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=98afa9a260a8b5e06df4800395d537e2"
    PARAMS = {'units': 'metric'}

    # -------- GOOGLE IMAGE API --------
    API_KEY = "AIzaSyAYBBQ0nPSEqC_55BlmuyoInT6CWVQRUi8"
    SEARCH_ENGINE_ID = "26cd83dd9c4724988"

    query = f"{city} 1920x1080"
    search_url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        f"&searchType=image&imgSize=xlarge"
    )

    # -------- GET CITY IMAGE --------
    image_url = None
    exception_occured = False

    try:
        img_res = requests.get(search_url).json()
        search_items = img_res.get("items", [])

        if len(search_items) > 0:
            image_url = search_items[0]["link"]  # safest index
        else:
            exception_occured = True

    except:
        exception_occured = True

    # -------- GET WEATHER DATA --------
    try:
        data = requests.get(WEATHER_URL, PARAMS).json()

        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        temp = data["main"]["temp"]
        day = datetime.date.today()

        return render(request, "weatherapp/index.html", {
            "description": description,
            "icon": icon,
            "temp": temp,
            "day": day,
            "city": city,
            "exception_occured": exception_occured,
            "image_url": image_url
        })

    except:
        
        messages.error(request, "Entered city is not available")

        return render(request, "weatherapp/index.html", {
            "description": "clear sky",
            "icon": "01d",
            "temp": 25,
            "day": datetime.date.today(),
            "city": "indore",
            "exception_occured": True,   # fallback background
            "image_url": None
        })
