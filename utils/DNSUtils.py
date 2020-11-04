def get_authority_domain(data):
    domain, offset = read_name_from_bytes(data)
    print(domain)
    return domain, offset


def read_name_from_bytes(data):
    state = 0
    expected_length = 0
    domain_string = ''
    domain_parts = []
    x = 0
    y = 0

    for byte in data:
        if state == 1:
            if byte != 0:
                domain_string += chr(byte)
            x += 1
            if x == expected_length:
                domain_parts.append(domain_string)
                domain_string = ''
                state = 0
                x = 0
            if byte == 0:
                domain_parts.append(domain_string)
                break
        else:
            state = 1
            expected_length = byte
        y += 1
    return domain_parts, y


def get_name_length(data):
    length = 0
    for byte in data:
        if byte == 0:
            break
        length += 1
    return length


def get_ipv4_addr(data):
    result = []
    for byte in data:
        result.append(str(byte))
    return '.'.join(result)

def get_ipv6_addr(data):
    pass
