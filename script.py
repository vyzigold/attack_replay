import sys

class AttackReader:
    def __init__(self, filename):
        self.f = open(filename, "rb")

    def get_sample(self):
        sample_type = self.f.read(1).decode("utf-8")
        if len(sample_type) == 0:
            return ("E", 0, b"")
        self.f.read(1) # shoud be ":"
        sample_size = None
        sample_size = int.from_bytes(self.f.read(4), byteorder='little')
        data = self.f.read(sample_size)
        return (sample_type, sample_size, data)

    def get_input_sample(self):
        t = "O"
        while t != "I" and t != "E":
            t, s, data = self.get_sample()
        return data.replace(b"\r", b"\n")

    def get_output_sample(self):
        t = "I"
        while t != "O" and t != "E":
            t, s, data = self.get_sample()
        return data

def show_output(filename):
    import termios, tty
    stdin = sys.stdin.fileno()
    tty.setcbreak(stdin, termios.TCSANOW)
    reader = AttackReader(filename)
    print("outputing")
    while len((sample := reader.get_sample())) != 0:
        sample_type, _, sample_data = sample
        if sample_type == "E":
            break
        if sample_type == "O":
            sys.stdout.write(sample_data.decode("utf-8"))
        sys.stdout.flush()
        sys.stdin.read(1)

def show_input(filename):
    reader = AttackReader(filename)
    while len((sample := reader.get_input_sample().decode("utf-8"))) != 0:
        print(sample, end='')

if len(sys.argv) != 3:
    print("use either --input or --output")

if sys.argv[1] == "--input":
    show_input(sys.argv[2])

if sys.argv[1] == "--output":
    show_output(sys.argv[2])
