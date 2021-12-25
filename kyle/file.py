import os


fREAD = 'r'
fWRITE = 'w'
fREAD_WRITE = 'rw'
fAPPEND = 'a'

class GameFileManager:

    def __init__(self, files=[]):
        self.files = []

    def add_file(self, file):
        pass

    def remove_file(self, file):
        pass

    def read_file(self, file):
        return self.file.c_line

    def get_file(self, name=None, path=None):
        if name:
            for file in self.files:
                if file.name == name:
                    return file
        else:
            raise NotImplementedError()

class GameFile:

    COMMENT_MARK = '#'
    SECTION_MARK = '@'
    SLOWTYPE_MARK = '~'
    NEXT_LEVEL = '&'
    NO_ACTION_REQUIRED = 0
    ACTION_REQUIRED = 1

    def __init__(self, file_name, io, access=fREAD):
        self.io = io
        # You better put the ext in it because I don't wanna be responsible
        self.file_name = file_name
        # Only doing CWD not any other location, nope - not my cup of dirty tea rn
        self.path = os.getcwd() + '\\' + self.file_name
        self.file = open(self.path, access)
        self.contents = self.file_contents(self.file)
        self.line_num = 0
        self.c_line = ''
        self.file.close()


    def next_line(self):
        self.c_line = self.contents[self.line_num]
        self.line_num += 1

        if self.c_line.startswith(self.COMMENT_MARK) or self.c_line.isspace() or self.c_line == '':
            return self.next_line()

        elif self.c_line.startswith(self.SECTION_MARK):
            self.c_line = ''
            stop_line = self.find_next_mark(self.line_num, GameFile.SECTION_MARK)
            for line in range(self.line_num, stop_line):
                self.c_line += self.contents[line] + '\n'
            self.line_num = stop_line + 1
            self.io.stdout(self.c_line)
            return self.NO_ACTION_REQUIRED

        elif self.c_line.startswith(self.SLOWTYPE_MARK):
            self.c_line = ''
            stop_line = self.find_next_mark(self.line_num, GameFile.SLOWTYPE_MARK)
            for line in range(self.line_num, stop_line):
                self.c_line += self.contents[line] + '\n'
            self.line_num = stop_line + 1
            self.io.typeout(self.c_line)
            return self.NO_ACTION_REQUIRED

        elif self.c_line.startswith(self.NEXT_LEVEL):
            return self.ACTION_REQUIRED
        else:
            return self.NO_ACTION_REQUIRED



    def find_next_mark(self, c_line_num, mark):
        for line_num, contents in self.contents.items():
            if contents.startswith(mark) and line_num > c_line_num:
                return line_num
        raise KeyError('Matching mark', mark, ' not found')


    def file_contents(self, file):
        dict = {}
        lines = file.readlines()
        for index, line in enumerate(lines):
            dict[index] = line.rstrip('\n')
        return dict
