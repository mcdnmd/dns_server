import socket
import threading

from modules.DNSLogic import DNSLogic


class Router:
    def __init__(self, host, port=53):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (host, port)
        self.threads = []
        self.DNSLogic = DNSLogic()
        self.lock = threading.Lock()

    def __enter__(self):
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)
        print('Server successfully binded!')
        return self

    def __exit__(self, *exc_info):
        self.server.close()
        for thread in self.threads:
            thread.join()
        return False

    def run(self):
        while True:
            data, client_addr = self.server.recvfrom(65535)
            t = threading.Thread(target=self._serve, args=(data,
                                                           client_addr))
            self.threads.append(t)
            t.start()

    def _serve(self, data, addr):
        print(f'Get data from {addr}')
        print(data)
        if data:
            response = self.DNSLogic.get_dns_info(data)
            with self.lock:
                self.server.sendto(response, addr)