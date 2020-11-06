# dns_server
It is a simple DNS server. Support all root ns servers.
Use `sudo python3 dns.py` to launch it.

## Components

* `modules.Router` - responsible for route multi-client server
* `modules.DNSMessages` - parsing and creation DNS messages
* `modules.DNSLogic` - the logic of DNS cycle. Try to get final answer for request.
* `utils.DNSUtils` - some general methods for decomposition
