import csv
import argparse
from binascii import Error


class Interpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.stack = []
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory = [0] * 1024
        self.memory_range = memory_range
        self.code = []
        self.stack = []

    def run(self):

        with open(self.binary_file, 'rb') as f:
            self.code = f.read()
        # Перевод бинарных данных в строку битов
        bits = ''.join(
            ''.join(f"{byte:08b}" for byte in self.code[i:i + 3][::-1])
            for i in range(0, len(self.code), 3)
        )
        # Разделение на команды длиной 24 бит (3 байта)
        commands = [bits[i:i + 24] for i in range(0, len(bits), 24)]
        for command in commands:
            command_type = int(command[-7:], 2)
            match command_type:
                case 45: # новый элемент в стеке (константа)
                    value = int(command[-18:-7], 2)
                    self.stack.append(value)
                case 80: # новый элемент в стеке (чтение из памяти по адресу)
                    address = int(command[-17:-7], 2)
                    value = self.memory[address]
                    self.stack.append(value)
                case 85: # элемент, снятый с вершины стека
                    address = int(command[-17:-7], 2)
                    value = self.stack.pop()
                    self.memory[address] = value
                case 40: #  ячейка памяти по адресу, снятого с вершины стека
                    if len(self.stack) == 0:
                        raise IndexError(f"Невозможно выполнить данную операцию")
                    value = self.stack.pop()
                    self.memory[value] = value
        self.save_results()


    def save_results(self):

        # Создаем список для записи в CSV
        data = []
        for i in range(*self.memory_range):
            value = self.memory[i]
            data.append({"0b" + bin(i)[2:].zfill(4): value})
        all_keys = set()
        for entry in data:
            all_keys.update(entry.keys())

        with open(self.result_file, 'w', newline='') as f:
            writer = csv.writer(f)

            for item in data:
                for key, value in item.items():
                    writer.writerow([key, value])



if __name__ == "__main__":
    parser = argparse.ArgumentParser('Interpreter')
    parser.add_argument('binary_path', type=str, help='The path to the binary file')
    parser.add_argument('output_path', type=str, help='The path to the output file')
    parser.add_argument('memory_range', nargs=2, type=int, help='the memory_range')

    args = parser.parse_args()

    inter =Interpreter(args.binary_path, args.output_path, tuple(args.memory_range))
    inter.run()
