# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3, web


# Airprot with autolookup

# Data source: http://ourairports.com/data/airports.csv

def main(wf):
    query = str(wf.args[0]).lower()
    log.debug(query)

    # "id","ident","type","name","latitude_deg","longitude_deg","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","gps_code","iata_code","local_code","home_link","wikipedia_link","keywords"
    with open('airports.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:

            if query in line.lower():

                parts = line.split(',')
                apt_id = parts[0][1:-1]
                icao = parts[1][1:-1]
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

                # print icao, iata_code, local_code, name, home_link, wikipedia_link
                codes = filter(None, set([icao, iata_code, gps_code, local_code]))
                # print name, codes
                # \\U0001F1F2\\U0001F1FD\\U0000FE0F
                flag = ""
                if len(iso_country) > 1:
                    l1 = str(hex(ord(iso_country[0]) + 127397)[2:]).upper()
                    l2 = str(hex(ord(iso_country[1]) + 127397)[2:]).upper()
                    flag = "\\U000{}\\U000{}\\U0000FE0F".format(l1, l2)
                # print iso_country, flag.decode('unicode_escape')

                # title = str(name + " " + flag)
                subtitle = ", ".join(codes) + " " + apt_type

                wf.add_item(str(name).decode('utf-8', 'ignore') + " " + flag.decode('unicode_escape'), subtitle, arg=icao, valid=True)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
