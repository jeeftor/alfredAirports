# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3
import urllib2, sys
import shutil

RUNWAY_URL  = 'http://ourairports.com/data/runways.csv'
AIRPORT_URL = 'http://ourairports.com/data/airports.csv'
FRQ_URL     = 'http://ourairports.com/data/airport-frequencies.csv'
NAVAID_URL  = 'http://ourairports.com/data/navaids.csv'


def main(wf):

    file_count = 0
    wf.store_data('download_progress', "%d/4" % file_count)

    for url in [AIRPORT_URL, RUNWAY_URL, FRQ_URL, NAVAID_URL]:
        file_count += 1
        file_name = url.split('/')[-1]
        wf.store_data('download_progress', "%d/4" % file_count)
        wf.store_data('download_file', file_name)
        download_file(url, file_name)


def download_file(url, file_name):

    file_url = url.lower()

    log.info("Downloading " + file_url)
    temp_filename = file_name + '.tmp'

    f = open(temp_filename, 'wb')
    remote_file = urllib2.urlopen(file_url)

    try:
        total_size = remote_file.info().getheader('Content-Length').strip()
        header = True
    except AttributeError:
        header = False  # a response doesn't always include the "Content-Length" header

    if header:
        total_size = int(total_size)

    bytes_so_far = 0

    while True:
        buffer = remote_file.read(1024)
        if not buffer:
            sys.stdout.write('\n')
            break

        bytes_so_far += len(buffer)
        f.write(buffer)
        if not header:
            total_size = bytes_so_far  # unknown size

        percent = float(bytes_so_far) / total_size
        percent = round(percent * 100, 2)
        log.info("%s Downloaded %d of %d bytes %0.2f%%\r" % (file_name, bytes_so_far, total_size, percent))
        #sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % (bytes_so_far, total_size, percent))
        wf.store_data('download_percent', "%0.1f%%" % percent)



    # Rename dl file to actual file
    shutil.move(temp_filename, file_name)

if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
