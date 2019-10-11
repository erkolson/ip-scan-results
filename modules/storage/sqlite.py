import sqlite3
import os
from libnmap.parser import NmapParser

if 'LOG_LEVEL' in os.environ:
    LOG_LEVEL = os.environ['LOG_LEVEL']
else:
    LOG_LEVEL = ''

support_ports = {'80', '443', '5000', '8080', '8443'}

# Setup database connection
connection = sqlite3.connect(":memory:", check_same_thread=False)
schema = "(ip text, hostname text, tcp80_state text, tcp80_reason text, tcp443_state text, tcp443_reason text, tcp5000_state text, tcp5000_reason text, tcp8080_state text, tcp8080_reason text, tcp8443_state text, tcp8443_reason text)"
c = connection.cursor()

# Check if the schema has been loaded
# returns true if ready
# returns false if not
def db_ready():
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='hosts'")
    status = c.fetchone()
    if status[0] == 1:
        return True
    else:
        return False

# ip = string, ip address
# hostname = string, hostname
# services = list of libnmap.objects.service
# https://libnmap.readthedocs.io/en/latest/objects/nmapservice.html
def store_ip(ip, hostname, services):
    # create a dict of port numbers and their state and reason
    ports = {}
    for service in services:
        service_dict = service.get_dict()
        if LOG_LEVEL == 'DEBUG' :
            print("{}".format(service_dict))
        ports[service_dict['port']] = { 'state': service_dict['state'], 'reason': service_dict['reason']}

    # now store the row
    c.execute("INSERT INTO hosts VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        ip,
        hostname,
        ports['80']['state'],
        ports['80']['reason'],
        ports['443']['state'],
        ports['443']['reason'],
        ports['5000']['state'],
        ports['5000']['reason'],
        ports['8080']['state'],
        ports['8080']['reason'],
        ports['8443']['state'],
        ports['8443']['reason'],
        ))

def load_db(file_path):
    records_stored = 0
    c.execute('DROP TABLE IF EXISTS hosts')
    c.execute("CREATE TABLE hosts {}".format(schema))
    # https://libnmap.readthedocs.io/en/latest/objects/nmapreport.html
    nmap_report = NmapParser.parse_fromfile(file_path)
    for scanned_host in nmap_report.hosts:
        host_ip = scanned_host.address
        hostnames = scanned_host.hostnames
        # ports and services are separate objects.  First get the ports
        ports = scanned_host.get_ports()
        # get the scan result for each port (a 'service')
        services = [scanned_host.get_service(port[0],port[1]) for port in ports]
        # if hostname is missing, make it an empty string
        hostname = ""
        if hostnames:
            hostname = hostnames[0]

        store_ip(host_ip, hostname, services)

        records_stored += 1

        if LOG_LEVEL == 'DEBUG' :
            print("ip: {}; hostnames: {}; ports: {}".format(host_ip, hostnames, ports))

    #TODO: actually look for errors!
    return (records_stored, nmap_report.summary)

def get_ip(ip):
    if db_ready():
        hostname = ""
        q = (ip,)
        c.execute('SELECT hostname FROM hosts WHERE ip=?',q)
        tuple = c.fetchone()
        if tuple:
            hostname = tuple[0]
        return hostname
    else:
        return ""

def get_host(ip):
    if db_ready():
        q = (ip,)
        c.execute('SELECT * FROM hosts WHERE ip=?',q)
        return c.fetchone()
    else:
        return ('','','','','','','','','','','','')

# Return tuples of all hosts with specified port open
def get_hosts_open_port(port):
    if db_ready():
        # lets not yolo with the db, check for valid ports and construct the
        # column name
        port_string = str(port)
        if port_string not in support_ports:
            print("ERROR: unsupported port {}".format(port))
            return 1
        col = "tcp{}_state".format(port_string)

        query = "SELECT * FROM hosts WHERE {} = 'open'".format(col)

        return [row for row in c.execute(query)]
    else:
        return []

def get_all():
    if db_ready():
        return [row for row in c.execute('SELECT * FROM hosts')]
    else:
        return []
