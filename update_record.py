import os
import sys
import json
import requests


class BaseAPI(object):

    def __init__(self):
        self.read_environment()
        self.server_ip = sys.argv[1]
        self.api_token = sys.argv[2]
        self.domain = sys.argv[3]
        self.a_record = sys.argv[4]
        self.api_endpoint = 'https://api.digitalocean.com/v2'
        self.headers = {'Authorization': 'Bearer {0}'.format(self.api_token),
                        'Content-type': 'application/json'}
        self.timeout = 60
        self.replace_ip(ip=self.server_ip)

    def read_environment(self):
        """ Reads the settings from environment variables """
        # Setup credentials
        if os.getenv("DO_API_TOKEN"):
            self.api_token = os.getenv("DO_API_TOKEN")
        if os.getenv("DO_API_KEY"):
            self.api_token = os.getenv("DO_API_KEY")
        if os.getenv("DOMAIN"):
            self.domain = os.getenv("DOMAIN")
        if os.getenv("A_RECORD"):
            self.a_record = os.getenv("A_RECORD")

    def _url_builder(self, path):
        if path[0] == '/':
            path = path[1:]
        return '%s/%s' % (self.api_endpoint, path)

    def send(self, url, method='GET', data=None):
        url = self._url_builder(url)
        data = json.dumps(data)
        try:
            resp_data = {}
            if method == 'GET':
                incomplete = True
                while incomplete:
                    resp = requests.get(url, data=data, headers=self.headers, timeout=self.timeout)
                    json_resp = resp.json()

                    for key, value in json_resp.items():
                        if isinstance(value, list) and key in resp_data:
                            resp_data[key] += value
                        else:
                            resp_data[key] = value

                    try:
                        url = json_resp['links']['pages']['next']
                    except KeyError:
                        incomplete = False

            if method == 'PUT':
                resp_data = requests.put(url, data=data, headers=self.headers, timeout=self.timeout)

        except ValueError as e:
            sys.exit("Unable to parse result from %s: %s" % (url, e))
        return resp_data

    def all_active_droplets(self):
        resp = self.send('droplets/')
        resp_droplets = resp['droplets']
        return resp_droplets

    def all_domains(self):
        resp = self.send('domains/{}/records/{}/'.format(self.domain, self.a_record))
        resp_domains = resp

    def retrieve_server_ip(self):
        self.all_domains()
        droplet_resp = self.all_active_droplets()
        for droplet in droplet_resp:
            if droplet['name'] == 'jitsi-server':
                ip_address = droplet['networks']['v4'][1]['ip_address']
                print(json.dumps(ip_address, indent=2))
        return ip_address

    def replace_ip(self, ip):
        #ip_addr = self.retrieve_server_ip()
        ip_addr = ip
        domain = self.domain
        a_record = self.a_record
        full_url = "domains/{}/records/{}/".format(domain, a_record)
        print(full_url)
        status = self.send(url=full_url, method='PUT', data={'data':ip_addr})
        print(status)

BaseAPI()