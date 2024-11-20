import argparse
import csv



class Assembler:

    def __init__(self, input_file, binary_file, log_file):
        self.input_file = input_file
        self.binary_file = binary_file
        self.log_file = log_file
        self.log_entries = []

    def log(self, text: dict, method="last"):
        if method == "last":
            self.log_entries.append(text)
        elif method == "append":
            self.log_entries[-1].update(text)

    def write_to_binary(self, bytes):
        logged = ", ".join([("0x" + hex(i)[2:].zfill(2).upper()).ljust(4, '0') for i in bytes])
        self.log({"bin": logged}, method="append")

        with open(self.binary_file, 'ab') as f:
            f.write(bytes)



    def write_log(self):
        all_keys = set()
        for entry in self.log_entries:
            all_keys.update(entry.keys())
        fieldnames = sorted(all_keys)

        with open(self.log_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if f.tell() == 0:
                writer.writeheader()

            writer.writerows(self.log_entries)

    # кодировка
    def int_to_hex(self, a, b=0):
        if b:
            self.log({"A": a, "B": b})
            # Формируем биты для команды с D
            a_bin = bin(a)[2:].zfill(7)
            if a == 45:
                b_bin = bin(b)[2:].zfill(11)
            else:
                b_bin = bin(b)[2:].zfill(10)
            s = b_bin + a_bin
        else:
            self.log({"A": a})
            # Формируем биты для команды без D
            a_bin = bin(a)[2:].zfill(7)
            s = a_bin
        s = s.zfill(24)
        return int(s, 2).to_bytes(3, "big")[::-1]

    def run(self):
        open(self.binary_file, 'w').close()
        open(self.log_file, 'w').close()

        with open(self.input_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                commands = line.strip().split()
                a = int(commands[0])
                b = 0
                if len(commands) > 1:
                    b = int(commands[1])
                binary = self.int_to_hex(a, b)
                self.write_to_binary(binary)
        self.write_log()



if __name__ == "__main__":
    parser = argparse.ArgumentParser('Assembler')
    parser.add_argument('input_path', type=str, help='The path to the input file')
    parser.add_argument('binary_path', type=str, help='The path to the binary file')
    parser.add_argument('log_path', type=str, help='The path to the log_file')

    args = parser.parse_args()
    assembler = Assembler(args.input_path, args.binary_path, args.log_path)
    assembler.run()


