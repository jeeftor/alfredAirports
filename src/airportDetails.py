# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3
from workflow.background import is_running

def main(wf):
    query = str(wf.args[0])
    log.debug(query)
    get_airport_details_from_icao(query)
    get_frequencies(query)
    wf.send_feedback()

def get_airport_details_from_icao(icao):
    found = False
    with open('airports.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:
            parts = line.split(',')
            if parts[1][1:-1].lower() == icao.lower():
                found = True
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

                flightaware = "http://flightaware.com/live/airport/" + icao.upper()
                fr24link = "https://www.flightradar24.com/%0.2f,%0.2f/12" % (float(latitude_deg),float(longitude_deg))
                google_link = 'https://www.google.com/maps/preview/@{},{},14z'.format(latitude_deg,longitude_deg)
                flag = ""
                if len(iso_country) > 1:
                    l1 = str(hex(ord(iso_country[0]) + 127397)[2:]).upper()
                    l2 = str(hex(ord(iso_country[1]) + 127397)[2:]).upper()
                    flag = "\\U000{}\\U000{}\\U0000FE0F".format(l1, l2)

                wf.add_item(str(name).decode('utf-8', 'ignore') + " " + flag.decode('unicode_escape'), municipality + ", " + iso_region)
                wf.add_item("Identifiers","ICAO: {} IATA: {} Local: {}it GPS: {}".format(icao, iata_code, local_code, gps_code), icon="images/icao.png")
                wf.add_item("Location", subtitle=lla, icon="images/map.png", valid=True, arg=google_link)

                # IF USA we have airnav
                if iso_country == "US":
                    airnav_link = 'http://www.airnav.com/airport/{}'.format(icao)
                    wf.add_item("Airnav", "Open " + airnav_link, arg=airnav_link, valid=True,
                                icon='images/airnav.png')


                fl = wf.add_item("See Flights", "Open flightradar 24",
                                 arg=fr24link,
                                 valid=True,
                                 icon="images/radar.png")
                fl.add_modifier("alt",subtitle="Open Flight Aware", arg=flightaware, valid=True)


                if wikipedia_link != "":
                    wf.add_item('Wiki','Open wikipedia link to airport', arg=wikipedia_link, icon="images/wiki.png", valid=True)



                if home_link != "":
                    hl_arg = home_link
                else:
                    hl_arg = 'http://ourairports.com/airports/' + icao.upper()
                hl = wf.add_item('Airport Website', 'Open the airports website', arg=hl_arg, icon="images/web.png", valid=True)
                hl.add_modifier("alt",subtitle='Edit the airport database', arg='http://ourairports.com/airports/' + icao.upper() + '/edit.html', valid=True)

                get_runways(icao)

    if not found:
        wf.add_item('No Data for ICAO: ' + icao.upper(),'The airport database does not have any info for this airport', valid=False, icon="images/evil.png")

def surface_decode(surface):

    return surface

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


                if len(le_ident) == 1:
                    le_ident = "0{}".format(le_ident)
                if len(he_ident) == 1:
                    he_ident = "0{}".format(he_ident)

                if "L" in le_ident:
                    img = "{}.png".format(le_ident)
                elif "L" in he_ident:
                    img = "{}.png".format(he_ident)
                if "C" in le_ident or "C" in he_ident:
                    img = "{}.png".format(min(le_ident,he_ident))
                elif "L" in he_ident:
                    img = "{}.png".format(he_ident)
                else:
                    img = "{}.png".format(min(le_ident,he_ident))

                title = "Runway {}/{}".format(le_ident,he_ident)
                subtitle = "Length: {} Width: {} Surface: {} Lights: {}".format(length_ft, width_ft, surface_decode(surface), lighted)

                wf.add_item(title,subtitle=subtitle, icon="images/runway/{}".format(img))



    ret = ", ".join(runways)


    # wf.add_item('Runways', subtitle=ret, icon="images/ryw/Left17.png", valid=False)


def get_frequencies(icao):
    import csv

    with open('airport-frequencies.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if icao.lower() in row["airport_ident"].lower():

                airport_id = row["id"]
                airport_ref = row["airport_ref"]

                type = row["type"]
                desc = row["description"]
                frq=row["frequency_mhz"]
                wf.add_item(desc, str(frq) + " mhz",icon="images/radio.png",valid=False)



if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
