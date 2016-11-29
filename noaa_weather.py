from noaaweather import weather
import bs4
sfWeather=weather.noaa();
print("\n enter your zip code");
zip=raw_input();
sfWeather.getByZip(zip);
a=sfWeather.temperature.apparent.value
b=float(a)
#print(sfWeather.temperature.apparent.value);
#soap=bs4.BeautifulSoup(a,"html.parser");
print(type(a));
print(b);
#print(soap.prettify());
