import gps

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


report = session.next()
result = {}
while not report['class'] == 'TPV':
    result['time'] = report.time
    result['lat'] = report.lat
    result['lon'] = report.lon
    return result