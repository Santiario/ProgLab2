__author__ = 'keithd'

import arduino_connect


# Codes for the 5 signals sent to this level from the Arduino

_dot = 1
_dash = 2
_symbol_pause = 3
_word_pause = 4
_reset = 5


# Morse Code Class
class mocoder():

# Note: the codes for dot and dash coming to Python via the serial port are 1 and 2, respectively, since those were most
# convenient at the Arduino level. However, I've switched to 0 and 1 in this dictionary, since it is a lot easier to
# read.  So O = dot, 1 = dash in the _morse_codes dictionary below.  You will need to remember that when looking
# up letters and digits in this dictionary.

    _morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
               '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
               '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
               '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}

    def __init__(self, sport=True):
        if sport:
            self.serial_port = arduino_connect.pc_connect()
        self.reset()
        self.decoding_loop()

    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''

    # This should receive an integer in range 0-3 from the Arduino via a serial port
    def read_one_signal(self,port=None):
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data

    # The signal returned by the serial port is one (sometimes 2) bytes, that represent characters of a string.  So,
    # a 2 looks like this: b'2', which is one byte whose integer value is the ascii code 50 (ord('2') = 50).  The use
    # of function int on the string converts it automatically.   But, due to latencies, the signal sometimes
    # consists of 2 ascii codes.  In that case, we need to pull out each of the codes and convert them separately using
    # chr (and then int).
    def get_character(self, symbol):

        try:
            character = mocoder._morse_codes[symbol]
            return character
        except:
            return 'X'


    def process_signal(self, signal):
        if signal == 0 or signal == 1:
            self.current_symbol += str(signal)
        elif signal == 2:
            self.current_word += self.get_character(self.current_symbol)
            self.current_symbol = ''
            print(self.current_message + self.current_word)
        elif signal == 3:
            self.current_word += self.get_character(self.current_symbol)
            self.current_symbol = ''
            self.current_message += self.current_word + ' '
            self.current_word = ''
            print(self.current_message + self.current_word)
        elif signal == 4:
            self.current_word += self.get_character(self.current_symbol)
            self.current_symbol = ''
            self.current_message += self.current_word + '. '
            self.current_word = ''
            print(self.current_message + self.current_word)
        elif signal == 5:
            self.reset()
            print("Reset!")
        else:
            print("Illegal input from Arduino!")



    def decoding_loop(self):
        while True:
            s = self.read_one_signal(self.serial_port)
            #print("Mottatt signal:",s)
            if len(s) == 2:
                self.process_signal((int(chr(s[0]))))
                self.process_signal(int(chr(s[1])))
            else:
                self.process_signal(int(s.strip()))


coder = mocoder()