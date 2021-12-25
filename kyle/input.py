import time
from resources.colors import Colors
import random
import sys
import os
os.system("cls")

class ErrorMessages:

    Messages = [
        "NO! Invalid input. Try again.",
        "Bruh enter something valid!",
        "Stop being a honky and enter a valid choice...",
        "You know what I'll enter a choice for you.",
        "Yeah...if you could please stop entering wrong inputs that would be great.",
        "I'm gonna have to ask you to stop being a sexy loser and enter a correct choice.",
        "WHAT'S THE DEAL? INVALID INVALID INVALID!",
        "LET ME THINK...HMM, STOP!",
        "BOOTY LICKER. NUT PICKER. Wow."
    ]

class InputManager:

    PROMPT_CURSOR = '| '
    ORIGINAL_COLOR = Colors.Cyan
    
    def __init__(self, *a, **k):
        self.is_prompting = False
        self.first_msg_rcvd = False
        self.c_input = None
        self.current_color = False
        self.typeout_speed = 100
        self.stdout(Colors.Cyan)

    def prompt(self, msg, title=False, choices=[], command=False, is_numeric=True, color=False):
        self.is_prompting = True
        old_color = self.current_color
        self.current_color = color

        invalid_inputs = 0
        valid_input = False
        self.stdoutln('\n')
        while not valid_input:
            # Set color
            if self.current_color:
                self.stdout(self.current_color)
            else:
                self.stdout(self.ORIGINAL_COLOR)

            # If not first message
            if not self.first_msg_rcvd:
                # Print border
                # self.stdoutln(self.border(len=len(title) if title else 10))
                # print title
                if title:
                    self.reverse_color_msg(title)
                # Print message
                self.stdoutln(msg + '\n')
                # Print command
                if command:
                    self.stdoutln(command)
                self.first_msg_rcvd = True

            # Get input
            self.c_input = input('|  ')

            # Check if valid
            if len(choices) == 0:
                sys.stdout.flush()
                break
            elif self.is_valid_input(self.c_input, choices, is_numeric):
                if is_numeric:
                    self.c_input = self.to_numeric(self.c_input)
                valid_input = True
            else:
                self.error_out(ErrorMessages.Messages[random.randrange(0, len(ErrorMessages.Messages)) if invalid_inputs > 3 else invalid_inputs], border=True)
                invalid_inputs += 1

        self.is_prompting = False
        self.first_msg_rcvd = False
        usr_choice = self.c_input
        self.c_input = None
        sys.stdout.flush()
        return usr_choice

    def set_color(self, color):
        self.current_color = color

    def reset_color(self):
        self.current_color = False
        self.stdout(Colors.Reset)

    def reverse_color_msg(self, msg, end="\n"):
        if not self.current_color:
            self.stdout(Colors.Reversed + self.ORIGINAL_COLOR + msg + Colors.Reset + self.ORIGINAL_COLOR + end)
        else:
            self.stdout(Colors.Reversed + self.current_color + msg + Colors.Reset + self.current_color + end)


    def color_msg(self, msg, color, end="\n"):
        self.stdout(color + msg + Colors.Reset + self.current_color if self.current_color else self.ORIGINAL_COLOR + end)

    def error_out(self, error_msg, border=False):
        error_msg += "\n"
        if border:
            bdr = self.border(char='*', len=len(error_msg), end="\n")
            self.color_msg(bdr + error_msg + bdr, Colors.Red)
        else:
            self.stdoutln(error_msg)
            self.color_msg(error_msg, Colors.Red)

    def border(self, char='█', len=50, end=''):
        return char * len + end

    def border_msg(self, msg, char='█', color=False):
        out = msg + "\n"
        bdr = self.border(char=char, len=max(len(i) for i in msg.split("\n")) // len(char), end="\n")
        self.color_msg(bdr + out + bdr, color if color else self.current_color, end="")

    def out(self, msg):
        if msg in [None, 0, '0']:
            return
        print(msg)

    def stdout(self, msg):
        if msg == None:
            return
        sys.stdout.write(msg)
        sys.stdout.flush()

    def stdoutln(self, msg=''):
        if msg == None:
            return
        sys.stdout.write(msg)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def typeout(self, msg, line_break=50):

        def _typeout(letter):
            self.stdout(letter)
            # time.sleep(random.randrange(1, 9) / self.typeout_speed) # ms


        i = 0 # beginning of word
        j = i # end of word
        k = 0 # col
        # Type out letters up to j
        while j < len(msg):
            # Determine if we should line break before the start of the next word

            # spaces
            while msg[j].isspace():
                j += 1
                k += 1
            # words
            try:
                while not msg[j].isspace() or msg[j] == '\n':
                    j += 1
                    k += 1
            except:
                break
            # End word if out of loop

            if k > line_break:
                _typeout('\n')
                k = 0

            for char in range(i, j + 1):
                if msg[char] == '^':
                    _typeout('\n')
                    k = 0
                elif msg[char] != '\n':
                    _typeout(msg[char])
                else:
                    _typeout(' ')

            i = j + 1

        if i < len(msg):
            for char in range(i, len(msg) - 1):
                if msg[char] == '^':
                    _typeout('\n')
                elif msg[char] != '\n':
                    _typeout(msg[char])

        self.stdoutln()

    def is_valid_input(self, msg, choices, is_numeric):
        if is_numeric:
            try:
                return int(msg) in choices
            except:
                return False
        else:
            return msg in choices

    def to_numeric(self, msg, to_int=True):
        try:
            return int(msg)
        except:
            raise ValueError()
