# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3


def main(wf):
    query = str(wf.args[0])
    log.debug(query)
    get_airport_details_from_icao(query)
    wf.send_feedback()

def get_airport_details_from_icao(icao):
    with open('airports.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:
            parts = line.split(',')
            if parts[1][1:-1].lower() == icao.lower():
                apt_type = parts[2].replace('"', '')
                name = parts[3].replace('"', '')
                latitude_deg = parts[4].replace('"', '')
                longitude_deg = parts[5].replace('"', '')
                elevation_ft = parts[6].replace('"', '')
                continent = parts[7].replace('"', '')
                iso_country = parts[8].replace('"', '')
                iso_region = parts[9].replace('"', '')
                municipality = parts[10].replace('"', '')
                scheduled_service = parts[11].replace('"', '')
                gps_code = parts[12].replace('"', '')
                iata_code = parts[13].replace('"', '')
                local_code = parts[14].replace('"', '')
                home_link = parts[15].replace('"', '')
                wikipedia_link = parts[16].replace('"', '')
                keywords = parts[17:]

                lla = "Lat: {} Lon: {} Alt: {} ft".format(latitude_deg, longitude_deg, elevation_ft)



                fr24link = "https://www.flightradar24.com/%0.2f/%0.2f/12" % (float(latitude_deg),float(longitude_deg))
                google_link = 'https://www.google.com/maps/preview/@{},{},14z'.format(latitude_deg,longitude_deg)
                flag = ""
                if len(iso_country) > 1:
                    l1 = str(hex(ord(iso_country[0]) + 127397)[2:]).upper()
                    l2 = str(hex(ord(iso_country[1]) + 127397)[2:]).upper()
                    flag = "\\U000{}\\U000{}\\U0000FE0F".format(l1, l2)

                wf.add_item(str(name).decode('utf-8', 'ignore') + " " + flag.decode('unicode_escape'), municipality + ", " + iso_region)
                wf.add_item('Runways', subtitle=get_runways(icao), icon="images/runway.png", valid=False)

                wf.add_item("Location", subtitle=lla, icon="images/map.png", valid=True, arg=google_link)

                # IF USA we have airnav
                if iso_country == "US":
                    airnav_link = 'http://www.airnav.com/airport/{}'.format(icao)
                    wf.add_item("Airnav", "Open " + airnav_link, arg=airnav_link, valid=True,
                                icon='http://thereviewsolution.com/img/rs/airnav.jpg')
                wf.add_item("See Flights", "Open flightradar 24", arg=fr24link, valid=True, icon="images/radar.png")

                if wikipedia_link != "":
                    wf.add_item('Wiki','Open wikipedia link to airport', arg=wikipedia_link, icon="images/wiki.png", valid=True)
                if home_link != "":
                    hl = wf.add_item('Airport Website', 'Open the airports website', arg=home_link, icon="images/web.png", valid=True)
                    hl.add_modifier("cmd",subtitle='Edit the airport database', arg='http://ourairports.com/airports/' + icao.upper() + '/edit.html', valid=True)
                else:
                    wf.add_item('Update Airport Info','Edit the airport database', icon="images/web.png", arg='http://ourairports.com/airports/' + icao.upper() + '/edit.html', valid=True)
    pass

def get_runways(icao):
    runways = set()
    with open('runways.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:
            parts = line.split(',')
            if parts[2][1:-1].lower() == icao.lower():
                apt_id = parts[0].replace('"', '')
                airport_ref = parts[1].replace('"', '')
                airport_ident = parts[2].replace('"', '')
                length_ft = parts[3].replace('"', '')
                width_ft = parts[4].replace('"', '')
                surface = parts[5].replace('"', '')
                lighted = parts[6].replace('"', '')
                closed = parts[7].replace('"', '')
                le_ident = parts[8].replace('"', '')
                le_latitude_deg = parts[9].replace('"', '')
                le_longitude_deg = parts[10].replace('"', '')
                le_elevation_ft = parts[11].replace('"', '')
                le_heading_degT = parts[12].replace('"', '')
                le_displaced_threshold_ft = parts[13].replace('"', '')
                he_ident = parts[14].replace('"', '')
                he_latitude_deg = parts[15].replace('"', '')
                he_longitude_deg = parts[16].replace('"', '')
                he_elevation_ft = parts[17].replace('"', '')
                he_heading_degT = parts[18].replace('"', '')
                he_displaced_threshold_ft = parts[19].replace('"', '')

                runways.add("{}/{}".format(le_ident,he_ident))

    return ", ".join(runways)

def get_frequencies(icao):
    pass


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
