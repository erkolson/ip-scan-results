import unittest
from modules.storage.sqlite import load_db, get_ip, get_host, get_hosts_open_port, get_all

class DbTest(unittest.TestCase):

    def test_loadDB(self):
        (num_stored, summary) = load_db("./test/data/nmap.results.xml")
        self.assertEqual(num_stored, 40)

    def test_getIP(self):
        (num_stored, summary) = load_db("./test/data/nmap.results.xml")
        hostname1 = get_ip("217.100.37.170")
        hostname2 = get_ip("178.148.177.151")
        hostname3 = get_ip("47.93.173.17")
        self.assertEqual(hostname1, "D96425AA.static.ziggozakelijk.nl")
        self.assertEqual(hostname2, "cable-178-148-177-151.dynamic.sbb.rs")
        self.assertEqual(hostname3, "")

    def test_getHost(self):
        (num_stored, summary) = load_db("./test/data/nmap.results.xml")
        status = load_db("./test/data/nmap.results.xml")
        host = get_host("217.100.37.170")
        self.assertEqual(host[1], "D96425AA.static.ziggozakelijk.nl")
        self.assertEqual(host[10], "filtered")
        self.assertEqual(host[11], "no-response")

    def test_getHostsOpenPort(self):
        (num_stored, summary) = load_db("./test/data/nmap.results.xml")
        hosts_5000 = get_hosts_open_port(5000)
        self.assertEqual(len(hosts_5000), 12)
        hosts_80 = get_hosts_open_port(80)
        self.assertEqual(len(hosts_80), 26)

    def test_getAll(self):
        (num_stored, summary) = load_db("./test/data/nmap.results.xml")
        hosts = get_all()
        self.assertEqual(len(hosts), 40)

if __name__ == '__main__':
    unittest.main()
