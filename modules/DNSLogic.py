import socket
import random
from modules.DNSMessages import DNSMessage


class DNSLogic:
    def __init__(self):
        self.root_dns_servers = ['a.root-servers.net', 'b.root-servers.net',
                                 'c.root-servers.net', 'd.root-servers.net',
                                 'e.root-servers.net', 'f.root-servers.net',
                                 'g.root-servers.net', 'h.root-servers.net',
                                 'i.root-servers.net', 'j.root-servers.net']
        self.random_root_server = self.root_dns_servers[
            random.randint(0, len(self.root_dns_servers) - 1)]

    def get_dns_info(self, data):
        while True:
            query = DNSMessage()
            query.initialize_message(data)
            requested_ip = socket.gethostbyname(self.random_root_server)
            request = query.get_message()

            while True:
                sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock2.sendto(request, (requested_ip, 53))
                buffer, addr = sock2.recvfrom(65535)
                sock2.close()
                print(f'Received {len(buffer)} bytes from {addr}')

                response = DNSMessage()
                response.initialize_message(buffer)
                domains = response.get_domains()
                if response.answers is not None:
                    return response.get_message()
                requested_ip = domains[random.randint(0, len(domains)-1)]
