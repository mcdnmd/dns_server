import socket
from modules.DNSMessages import DNSMessage


class ServerRouter:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 53
        self.root_dns_servers = ['a.root-servers.net', 'b.root-servers.net',
                                 'c.root-servers.net', 'd.root-servers.net',
                                 'e.root-servers.net', 'f.root-servers.net',
                                 'g.root-servers.net', 'h.root-servers.net',
                                 'i.root-servers.net', 'j.root-servers.net']

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.ip, self.port))

            while True:
                data, addr = sock.recvfrom(65535)
                print(f'Received {len(data)} bytes')
                query = DNSMessage()
                query.initialize_message(data)
                requested_ip = socket.gethostbyname(self.root_dns_servers[3])
                request = query.get_message()

                while True:
                    # send request for root_dns_server
                    print(f'Sending udp to {requested_ip}')
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock2.setsockopt(socket.SOL_SOCKET,
                                         socket.SO_REUSEADDR, 1)
                    sock2.sendto(request, (requested_ip, 53))
                    buffer = sock2.recv(65535)
                    sock2.close()
                    print(f'Recived {len(buffer)} bytes')

                    response = DNSMessage()
                    response.initialize_message(buffer)
                    domains = response.get_domains()
                    if response.answers is not None:
                        print('Find answer!')
                        sock.sendto(response.get_message(), addr)
                        break
                    requested_ip = domains[0]
                break



def main():
    server = ServerRouter()
    server.run()


if __name__ == '__main__':
    main()
