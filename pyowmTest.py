from pyowm.owm import OWM
owm = OWM('617074221fda70c92dfe63c06b1ddf6a')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=52.5244, lon=13.4105)
national_weather_alerts = one_call. national_weather_alerts

for alert in national_weather_alerts:
    alert.sender                      # issuing national authority
    alert.title                       # brief description
    alert.description                 # long description
    alert.start_time()                # start time in UNIX epoch
    alert.end_time(timeformat='ISO')  # end time in ISO format
