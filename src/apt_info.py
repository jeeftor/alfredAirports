# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3


def main(wf):
    query = str(wf.args[0])
    log.debug(query)
    get_airport_details_from_icao(query)
    wf.add_item('Runways', subtitle=get_runways(query))
    wf.send_feedback()

def get_airport_details_from_icao(icao):
    with open('airports.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:
            parts = line.split(',')
            if parts[1][1:-1].lower() == icao.lower():
                apt_type = parts[2][1:-1]
                name = parts[3][1:-1]
                latitude_deg = parts[4][1:-1]
                longitude_deg = parts[5][1:-1]
                elevation_ft = parts[6][1:-1]
                continent = parts[7][1:-1]
                iso_country = parts[8][1:-1]
                iso_region = parts[9][1:-1]
                municipality = parts[10][1:-1]
                scheduled_service = parts[11][1:-1]
                gps_code = parts[12][1:-1]
                iata_code = parts[13][1:-1]
                local_code = parts[14][1:-1]
                home_link = parts[15][1:-1]
                wikipedia_link = parts[16][1:-1]
                keywords = parts[17:]

                lla = "Lat: {} Lon: {} Alt: {} ft".format(latitude_deg, longitude_deg, elevation_ft)


                flag = ""
                if len(iso_country) > 1:
                    l1 = str(hex(ord(iso_country[0]) + 127397)[2:]).upper()
                    l2 = str(hex(ord(iso_country[1]) + 127397)[2:]).upper()
                    flag = "\\U000{}\\U000{}\\U0000FE0F".format(l1, l2)

                wf.add_item(str(name).decode('utf-8', 'ignore') + " " + flag.decode('unicode_escape'), municipality + ", " + iso_region)
                wf.add_item("Location", subtitle=lla)
                wf.add_item('Wiki', wikipedia_link)
                wf.add_item('home_link', home_link)
    pass

def get_runways(icao):
    runways = set()
    with open('runways.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:
            parts = line.split(',')
            if parts[2][1:-1].lower() == icao.lower():
                apt_id = parts[0][1:-1]
                airport_ref = parts[1][1:-1]
                airport_ident = parts[2][1:-1]
                length_ft = parts[3][1:-1]
                width_ft = parts[4][1:-1]
                surface = parts[5][1:-1]
                lighted = parts[6][1:-1]
                closed = parts[7][1:-1]
                le_ident = parts[8][1:-1]
                le_latitude_deg = parts[9][1:-1]
                le_longitude_deg = parts[10][1:-1]
                le_elevation_ft = parts[11][1:-1]
                le_heading_degT = parts[12][1:-1]
                le_displaced_threshold_ft = parts[13][1:-1]
                he_ident = parts[14][1:-1]
                he_latitude_deg = parts[15][1:-1]
                he_longitude_deg = parts[16][1:-1]
                he_elevation_ft = parts[17][1:-1]
                he_heading_degT = parts[18][1:-1]
                he_displaced_threshold_ft = parts[19][1:-1]

                runways.add("{}/{}".format(le_ident,he_ident))

    return ", ".join(runways)

def get_frequencies(icao):
    pass


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
