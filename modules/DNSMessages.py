from utils.DNSUtils import get_authority_domain, read_name_from_bytes, \
    get_ipv4_addr, get_name_length

"""
    DNS message format
    
    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+
    |      Authority      | RRs pointing toward an authority
    +---------------------+
    |      Additional     | RRs holding additional information
    +---------------------+
"""

"""
    Header section format
    
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""


class Header:
    def __init__(self):
        # ID START
        self.ID = None
        # ID END

        # FLAGS START
        self.QR = None
        self.OPCODE = None
        self.AA = None  # should be 0
        self.TC = None
        self.RD = None
        self.RA = None
        self.Z = None  # should be 000
        self.RCODE = None
        # FLAGS END

        # COUNTERS START
        self.QDCOUNT = None
        self.ANCOUNT = None
        self.NSCOUNT = None
        self.ARCOUNT = None
        # COUNTERS END
        self.nextblock = 12

        self.header_in_bytes = None

    def extract_headers(self, data):
        self.ID = data[:2]
        self.extract_flags(data[2:4])
        self.extract_counters(data[4:12])
        self.create_bytes_header()

    def extract_flags(self, data):
        byte1 = self.convert_byte_to_bit(bin(ord(data[:1])).lstrip('0b'))
        byte2 = self.convert_byte_to_bit(bin(ord(data[1:2])).lstrip('0b'))
        self.QR = str(byte1[0])
        self.OPCODE = ''
        for bit in byte1[1:5]:
            self.OPCODE += str(bit)
        self.AA = str(byte1[5])
        self.TC = str(byte1[6])
        self.RD = str(byte1[7])
        self.RA = str(byte2[0])
        self.Z = ''
        for bit in byte2[1:4]:
            self.Z += str(bit)
        self.RCODE = ''
        for bit in byte2[4:8]:
            self.RCODE += str(bit)

    def extract_counters(self, data):
        self.QDCOUNT = data[0:2]
        self.ANCOUNT = data[2:4]
        self.NSCOUNT = data[4:6]
        self.ARCOUNT = data[6:10]

    @staticmethod
    def convert_byte_to_bit(byte):
        n = len(byte)
        result = []
        for i in range(0, 8 - n):
            result.append(0)
        for i in range(0, n):
            result.append(byte[i])
        return result

    def convert_flags(self):
        return int(self.QR + self.OPCODE + self.AA + self.TC + self.RD,
                   2).to_bytes(1, byteorder='big') + int(
            self.RA + self.Z + self.RCODE, 2).to_bytes(1, byteorder='big')

    def create_bytes_header(self):
        self.header_in_bytes = b''
        self.header_in_bytes += self.ID
        self.header_in_bytes += self.convert_flags()
        self.header_in_bytes += self.QDCOUNT
        self.header_in_bytes += self.ANCOUNT
        self.header_in_bytes += self.NSCOUNT
        self.header_in_bytes += self.ARCOUNT

    def get_qdcount(self):
        return ord(self.QDCOUNT[:1]) + ord(self.QDCOUNT[1:2])

    def get_ancoute(self):
        return ord(self.ANCOUNT[:1]) + ord(self.ANCOUNT[1:2])

    def get_nscount(self):
        return ord(self.NSCOUNT[:1]) + ord(self.NSCOUNT[1:2])

    def get_arcount(self):
        return ord(self.ARCOUNT[:1]) + ord(self.ARCOUNT[1:2])

    def get_header(self):
        return self.header_in_bytes


"""
    Question section format
    
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""


class Question:
    def __init__(self):
        self.QNAME = None
        self.QTYPE = None
        self.QCLASS = None
        self.nextblock = 4

        self.question_in_bytes = None

    def extract_question(self, data):
        self.QNAME, length = read_name_from_bytes(data)
        self.QTYPE = data[length: length + 2]
        self.QCLASS = data[length + 2: length + 4]
        self.nextblock += length
        self.create_bytes_question()

    def create_bytes_question(self):
        self.question_in_bytes = b''
        for part in self.QNAME:
            length = len(part)
            self.question_in_bytes += bytes([length])
            for char in part:
                self.question_in_bytes += ord(char).to_bytes(1,
                                                             byteorder='big')

        self.question_in_bytes += self.QTYPE
        self.question_in_bytes += self.QCLASS

    def get_question(self):
        return self.question_in_bytes


""" 
    Resource record format
    
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""


class Answer:
    def __init__(self):
        self.NAME = None
        self.TYPE = None
        self.CLASS = None
        self.TTL = None
        self.RDLENGTH = None
        self.RDATA = None
        self.domain = None
        self.nextblock = 10

        self.answer_in_bytes = None

    def extract_answer(self, rawdata):
        data = rawdata
        length = get_name_length(data)
        self.nextblock += length
        self.NAME = data[:length]

        data = data[length:]

        self.TYPE = data[0:2]
        self.CLASS = data[2:4]
        self.TTL = data[4:8]
        self.RDLENGHT = data[8:10]
        data_length = ord(self.RDLENGHT[:1]) + ord(self.RDLENGHT[1:2])
        self.domain, domain_length = get_authority_domain(
            data[10:10 + data_length])

        self.RDATA = data[10: 10 + data_length]
        self.nextblock += data_length
        self.create_bytes_answer()

    def create_bytes_answer(self):
        self.answer_in_bytes = b''
        self.answer_in_bytes += self.NAME
        self.answer_in_bytes += self.TYPE
        self.answer_in_bytes += self.CLASS
        self.answer_in_bytes += self.TTL
        self.answer_in_bytes += self.RDLENGHT
        self.answer_in_bytes += self.RDATA

    def get_answer(self):
        return self.answer_in_bytes


class Authority:
    def __init__(self):
        self.NAME = None
        self.TYPE = None
        self.CLASS = None
        self.TTL = None
        self.RDLENGTH = None
        self.RDATA = None
        self.nextblock = 10

        self.authority_in_bytes = None

    def extract_authority(self, rawdata):
        data = rawdata
        length = get_name_length(data)
        self.nextblock += length
        self.NAME = data[:length]
        data = data[length:]

        self.TYPE = data[0:2]
        self.CLASS = data[2:4]
        self.TTL = data[4:8]
        self.RDLENGHT = data[8:10]
        data_length = ord(self.RDLENGHT[:1]) + ord(self.RDLENGHT[1:2])
        self.RDATA = data[10: 10 + data_length]
        self.nextblock += data_length
        self.create_bytes_authority()

    def create_bytes_authority(self):
        self.authority_in_bytes = b''
        self.authority_in_bytes += self.NAME
        self.authority_in_bytes += self.TYPE
        self.authority_in_bytes += self.CLASS
        self.authority_in_bytes += self.TTL
        self.authority_in_bytes += self.RDLENGHT
        self.authority_in_bytes += self.RDATA

    def get_authority(self):
        return self.authority_in_bytes


class Additional:
    def __init__(self):
        self.NAME = None
        self.TYPE = None
        self.CLASS = None
        self.TTL = None
        self.RDLENGTH = None
        self.RDATA = None
        self.domain = None
        self.nextblock = 10

        self.additional_in_bytes = None

    def extract_additional(self, rawdata):
        data = rawdata
        length = get_name_length(data)
        self.nextblock += length
        self.NAME = data[:length]
        data = data[length:]

        self.TYPE = data[0:2]
        self.CLASS = data[2:4]
        self.TTL = data[4:8]
        self.RDLENGHT = data[8:10]
        data_length = ord(self.RDLENGHT[:1]) + ord(self.RDLENGHT[1:2])
        if data_length == 4:
            self.domain = get_ipv4_addr(data[10:10 + data_length])
        self.RDATA = data[10: 10 + data_length]
        self.nextblock += data_length
        self.create_bytes_additional()

    def extract_extended_addition(self, rawdata):
        self.additional_in_bytes = b''
        self.additional_in_bytes += rawdata

    def create_bytes_additional(self):
        self.additional_in_bytes = b''
        self.additional_in_bytes += self.NAME
        self.additional_in_bytes += self.TYPE
        self.additional_in_bytes += self.CLASS
        self.additional_in_bytes += self.TTL
        self.additional_in_bytes += self.RDLENGHT
        self.additional_in_bytes += self.RDATA

    def get_additional(self):
        return self.additional_in_bytes


class DNSMessage:
    def __init__(self):
        self.header = None
        self.questions = None
        self.answers = None
        self.netservers = None
        self.additional = None

    def initialize_message(self, data):
        self.header = Header()
        self.header.extract_headers(data[:12])

        # Fill question field
        amount_questions = self.header.get_qdcount()
        pointer = self.init_questions(amount_questions, data)

        # Fill answers field. Should be None if not exists
        amount_answers = self.header.get_ancoute()
        pointer = self.init_answers(amount_answers, data, pointer)

        # Fill authority field. Should be None if not exists
        amount_authorities = self.header.get_nscount()
        pointer = self.init_netservers(amount_authorities, data, pointer)

        # Fill additions field. Should be None if not exists
        amount_additions = self.header.get_arcount()
        self.init_additions(amount_additions, data, pointer)

    def init_questions(self, n, data):
        self.questions = []
        pointer = 12
        for _ in range(n):
            question = Question()
            question.extract_question(data[pointer:])
            pointer += question.nextblock
            self.questions.append(question)
        return pointer

    def init_answers(self, n, data, pointer):
        if n == 0:
            return pointer
        self.answers = []
        for _ in range(n):
            answer = Answer()
            answer.extract_answer(data[pointer:])
            pointer += answer.nextblock
            self.answers.append(answer)
        return pointer

    def init_netservers(self, n, data, pointer):
        if n == 0:
            return pointer
        self.netservers = []
        for _ in range(n):
            netserver = Authority()
            netserver.extract_authority(data[pointer:])
            pointer += netserver.nextblock
            self.netservers.append(netserver)
        return pointer

    def init_additions(self, n, data, pointer):
        if n == 0:
            return pointer
        elif n == 1:
            self.additional = []
            additional = Additional()
            additional.extract_extended_addition(data[pointer:])
            self.additional.append(additional)
        else:
            self.additional = []
            for i in range(n):
                additional = Additional()
                if i == n - 1:
                    additional.extract_extended_addition(data[pointer:])
                else:
                    additional.extract_additional(data[pointer:])
                    pointer += additional.nextblock
                self.additional.append(additional)

    def get_domains(self):
        result = []
        try:
            for i in range(len(self.additional)):
                if self.additional[i].domain is not None:
                    result.append(self.additional[i].domain)
            return result
        except Exception as e:
            raise

    def get_message(self):
        message = b''
        message += self.header.get_header()

        if self.questions is not None:
            for i in range(len(self.questions)):
                message += self.questions[i].get_question()

        if self.answers is not None:
            for i in range(len(self.answers)):
                message += self.answers[i].get_answer()

        if self.netservers is not None:
            for i in range(len(self.netservers)):
                message += self.netservers[i].get_authority()

        if self.additional is not None:
            for i in range(len(self.additional)):
                message += self.additional[i].get_additional()

        return message
