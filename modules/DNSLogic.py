import socket

from modules.DNSMessages import DNSMessage


class DNSLogic:
    def __init__(self):
        self.root_dns_servers = ['a.root-servers.net', 'b.root-servers.net',
                                 'c.root-servers.net', 'd.root-servers.net',
                                 'e.root-servers.net', 'f.root-servers.net',
                                 'g.root-servers.net', 'h.root-servers.net',
                                 'i.root-servers.net', 'j.root-servers.net']

    def get_dns_info(self, data):
        while True:
            query = DNSMessage()
            query.initialize_message(data)
            requested_ip = socket.gethostbyname(self.root_dns_servers[3])
            request = query.get_message()

            while True:
                # send request for root_dns_server
                print(f'Sending udp to {requested_ip}')
                sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock2.sendto(request, (requested_ip, 53))
                buffer = sock2.recv(65535)
                sock2.close()
                print(f'Recived {len(buffer)} bytes')

                response = DNSMessage()
                response.initialize_message(buffer)
                domains = response.get_domains()
                if response.answers is not None:
                    print('Find answer!')
                    return response.get_message()
                requested_ip = domains[0]