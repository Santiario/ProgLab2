import abc


__author__ = 'Vemund'


class Coder:
    __metaclass__ = abc.ABCMeta

    def gen_message_from_file(self, filepath):
        pass

    def encode_decode_test(self, message):
        pass

    @abc.abstractmethod
    def encode(self, str):
        raise NotImplementedError("Please Implement this method")

    def decode(self, bits):
        raise NotImplementedError("Please Implement this method")


class AsciiCoder(Coder):

    def encode(self, str):
        pass

    def decode(self, bits):
        pass



if __name__ == '__main__':
    print('Hello world!')
