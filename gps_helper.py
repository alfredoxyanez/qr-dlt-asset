import gps


def get_gps():
    # Listen on port 2947 (gpsd) of localhost
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    report = session.next()
    result = {}
    while True:
        if report['class'] == 'TPV':
            if hasattr(report, 'time') and hasattr(report, 'lat') and hasattr(report, 'lon'):
                result['time'] = report.time
                result['lat'] = report.lat
                result['lon'] = report.lon
                break
        report = session.next()
    return result
