import abc

__author__ = 'Vemund'


class Coder:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def gen_message_from_file(filepath):
        file = open(filepath, 'r')
        message = file.read()
        file.close()
        return message.lower()

    def encode_decode_test(self, message):
        print('The original message was:\n' + message)
        encoded = self.encode(message)
        print('The encoded message is:\n' + encoded)
        decoded = self.decode(encoded)
        print('The decoded message is:\n' + decoded)
        print()
        print('The length of the original, encoded and decoded message, respectively:\n' +
              str(len(message))+' |', str(len(encoded))+' |', str(len(decoded)))
        if message == decoded:
            print('The message and decoded message match each other.')
            print('The compression rate is', str(self.compression_rate(len(message), len(encoded)))+'%')
        else:
            print('The message and decoded message do NOT match each other.')
            print('The compression rate is irrelevant. Fix your code first.')

    @abc.abstractmethod
    def encode(self, string):
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def decode(self, bits):
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def compression_rate(self, message_length, encoded_length):
        raise NotImplementedError("Please Implement this method")


class AsciiCoder(Coder):
    def encode(self, string):
        result = ''
        for char in string:
            code = bin(ord(char))
            code = code[0] + code[2:]
            code = '0'*(8-len(code)) + code  # Legger til 0'er foran teksten om den ikke er 8 siffer lang
            result += code
        return result

    def decode(self, bits):
        if len(bits) % 8 != 0:
            raise RuntimeWarning()
        result = ''
        index = 0
        while index < len(bits):
            result += chr(int(bits[index:index+8], 2))
            index += 8
        return result

    def compression_rate(self, message_length, encoded_length):
        return 1 - float(encoded_length)/(8*message_length)


if __name__ == '__main__':
    coder = AsciiCoder()
    coder.encode_decode_test(coder.gen_message_from_file('rings_bit.txt'))
