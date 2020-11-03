def decompose_id_from_bytes(data):
    string = ''
    for byte in data:
        string += hex(byte)[2:]
    return string


def decompose_flags_from_bytes(flags):
    byte1 = get_binary_expression(bin(ord(flags[:1])).lstrip('0b'))
    byte2 = get_binary_expression(bin(ord(flags[1:2])).lstrip('0b'))
    QR = str(byte1[0])
    OPCODE = ''
    for bit in byte1[1:5]:
        OPCODE += str(bit)
    AA = str(byte1[5])
    TC = str(byte1[6])
    RD = str(byte1[7])

    RA = str(byte2[0])
    Z = ''
    for bit in byte2[1:4]:
        Z += str(bit)
    RCODE = ''
    for bit in byte2[4:8]:
        RCODE += str(bit)

    return QR, OPCODE, AA, TC, RD, RA, Z, RCODE


def get_binary_expression(data):
    n = len(data)
    result = []
    for i in range(0, 8 - n):
        result.append(0)
    for i in range(0, n):
        result.append(data[i])
    return result


def get_question_domain(data):
    domain_parts, y = read_name_from_bytes(data)
    question_type = data[y:y + 2]
    question_class = data[y + 2:y + 4]
    return domain_parts, question_type, question_class, y + 16


def decompose_counts(data):
    question_bytes = data[0:2]
    answerRRs = data[2:4]
    authorityRRs = data[4:6]
    additionalRRs = data[6:10]
    return question_bytes, answerRRs, authorityRRs, additionalRRs


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
