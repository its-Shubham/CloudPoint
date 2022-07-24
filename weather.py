from tkinter import *
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import sqlite3

root = Tk()
root.title("Weather App")
root.geometry("900x500")
root.resizable(False, False)


class Weather:

    def __init__(self): 
        self.wind = None    #current instance
        self.humidity = None
        self.pressure = None
        self.temp = None
        self.description = None
        self.condition = None
        self.json_data = None
        self.current_time = None
        self.local_time = None
        self.home = None
        self.lat = None
        self.lng = None
        self.result = None
        self.obj = None
        self.location = None
        self.geolocator = None
        self.city = None
        
    def getweather(self):
        try:
            self.city = city.get()
            # Location & time                                                 #geopy is a Python client for several popular geocoding web services.
            self.geolocator = Nominatim(user_agent="weatherapp_mca")         #User_Agent is an http request header that is sent with each request.                                                                                    
            self.location = self.geolocator.geocode(self.city)                #geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources.
            self.obj = TimezoneFinder()
            self.result = self.obj.timezone_at(lng=self.location.longitude, lat=self.location.latitude)
            self.home = pytz.timezone(self.result)
            self.local_time = datetime.now(self.home)
            self.current_time = self.local_time.strftime("%I:%M %p")
            clock.config(text=self.current_time)
            name.config(text="CURRENT WEATHER")

            # weather
            self.lng = self.location.longitude
            self.lat = self.location.latitude
            api = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lng}&appid=99f687b165ae58cc5e045ca272011e58"

            self.json_data = requests.get(api).json()
            
            self.condition = self.json_data['weather'][0]['main']
            self.description = self.json_data['weather'][0]['description']
            self.temp = int(self.json_data['main']['temp'] - 273.15)
            self.pressure = self.json_data['main']['pressure']
            self.humidity = self.json_data['main']['humidity']
            self.wind = self.json_data['wind']['speed']

            t.config(text=(self.temp, "°"))
            c.config(text=(self.condition, "|", "FEELS", "LIKE", self.temp, "°"))

            w.config(text=self.wind)
            h.config(text=self.humidity)
            d.config(text=self.description)
            p.config(text=self.pressure)

        except Exception:
            messagebox.showerror("Weather App", "Invalid Entry!!")

    def save(self):
        con = sqlite3.connect("weather.db")
        cur = con.cursor()
        cur.execute("INSERT INTO WeatherData VALUES (:city,:temp,:condition,:wind,:humidity,:description,:pressure)",
                    {
                        'city': self.city,
                        'temp': self.temp,
                        'condition': self.condition,
                        'wind': self.wind,
                        'humidity': self.humidity,
                        'description': self.description,
                        'pressure': self.pressure
                    }
                    )

        con.commit()
        con.close()


city=StringVar()

# search box
Search_image = PhotoImage(file="search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = Entry(root,textvariable=city, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()
#------------------------
weatherobj = Weather()
# search_button
Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=weatherobj.getweather)
myimage_icon.place(x=400, y=34)

# logo
Logo_image = PhotoImage(file="logo.png")
logo = Label(image=Logo_image)
logo.place(x=150, y=100)

# Bottom box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# label
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)
label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)
label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)
label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)
t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
p.place(x=670, y=430)

# save
saveLabel = Label(text="SAVE", font=("arial", 20, 'bold'), fg="grey")
saveLabel.place(x=595, y=80)

Save_image = PhotoImage(file="save.png")
b1 = Button(image=Save_image, borderwidth=0, cursor="hand2", command=weatherobj.save)
b1.place(x=600, y=15)


def main():
    root.mainloop()


if __name__ == '__main__':
    main()