import json
import sys
import re


kol_bracket = 0
kol_array = 0
constants = {}
result = ""
in_dict = False
in_array = False
cur_value = ''
cur_name = ''

def calculating_constant(expression):
    if expression in constants:
        return constants[expression]
    else:
        return None

def parse_brackets(new_kol_bracket, line, num):
    global kol_bracket, in_dict
    kol_bracket = new_kol_bracket

    if kol_bracket > 0:
        in_dict = True
    if kol_bracket == 0:
        in_dict = False
    if kol_bracket < 0:
        raise SyntaxError(f"Ожидается {'{'} : {line} (строка {num + 1})")

def parse_brackets_array(new_kol_array, line, num):
    global kol_array, in_array
    kol_array = new_kol_array

    if kol_array > 0:
        in_array = True
    if kol_array == 0:
        in_array = False
    if kol_array < 0:
        raise SyntaxError(f"Ожидается {'('} : {line} (строка {num + 1})")

def parse_value(value, line, num, name):
    global result, cur_value, in_array

    if value == "":
        raise SyntaxError(f"Пустое значение константы: {line} (строка {num + 1})")

    elif value.startswith("'("):
        parse_brackets_array(kol_array+1, line, num)
        result += "[ "
        cur_value += '[ '
        value = value.strip()
        values = line[2:].split()
        for v in values:
            str_match = re.search(r'".+"', v)
            if str_match:
                if str_match[0] != v:
                    raise SyntaxError(f"Неверная запись строки: {line} (строка {num + 1})")
                result += f'{v}, '
                cur_value += f'{v}, '
                continue
            num_match = re.search(r"\d+\.?\d*", v)
            if num_match:
                if num_match[0] != v:
                    raise SyntaxError(f"Неверная запись числа: {line} (строка {num + 1})")

                result += f'{v}, '
                cur_value += f'{v}, '
                continue
            exp_match = re.search(r"\.[A-Z]+\.", v)
            if exp_match:
                expression = exp_match[0].strip('.')
                res = calculating_constant(expression)
                if res is None:
                    # Синтаксические ошибки выявляются с выдачей сообщений.
                    raise SyntaxError(f"Неверное выражение: {expression} (строка {num + 1})")
                else:
                    # line = line.replace(exp_match[0], res)
                    result += str(res) + ', '
                    cur_value += str(res) + ', '
                    continue
            else:
                value = v

    if value.startswith(")"):
        parse_brackets_array(kol_array-1, line, num)
        if result[-2] == ",":
            result = result[:-2] + ' '
            cur_value = cur_value[:-2] + ' '

        # result += (kol_bracket+1) * '  ' + "]"
        # cur_value += (kol_bracket+1) * '  ' + ']'
        result += "]"
        cur_value += ']'
        if not in_array:
            if value[1] != ";":
                raise SyntaxError(f"Неверная запись строки: {line} (строка {num + 1})")
            elif not in_dict:
                result += "\n}\n"
                constants[cur_name] = cur_value
                cur_value = ''
                return
            else:
                result += '\n'
                cur_value += '\n'
        value = value[1:]

    if value == "{":

        result += "{\n"
        cur_value += "{\n"
        parse_brackets(kol_bracket + 1, line, num)
    else:
        if value[-1] != ";":
            raise SyntaxError(f"Неверный формат: {line} (строка {num + 1})")
        value = value.strip(";")
        str_match = re.search(r'".+"', value)
        if str_match:
            if str_match[0] != value:
                raise SyntaxError(f"Неверная запись строки: {line} (строка {num + 1})")

            if not in_dict:
                constants[name] = value
                result += f'{value}' + "\n}\n"
            else:
                result += f'{value},\n'
                cur_value += f'{value},\n'
            return
        num_match = re.search(r"\d+\.?\d*", value)
        if num_match:
            if num_match[0] != value:
                raise SyntaxError(f"Неверная запись числа: {line} (строка {num + 1})")

            if not in_dict:
                constants[name] = float(value)
                result += f'{value}' + "\n}\n"
            else:
                result += f'{value},\n'
                cur_value += f'{value},\n'
            return
        exp_match = re.search(r"\.[A-Z]+\.", value)
        if exp_match:
            expression = exp_match[0].strip('.')
            res = calculating_constant(expression)
            if res is None:
                # Синтаксические ошибки выявляются с выдачей сообщений.
                raise SyntaxError(f"Неверное выражение: {expression} (строка {num + 1})")
            else:
                # line = line.replace(exp_match[0], res)
                if not in_dict:
                    result += str(res) + "\n}\n"
                    cur_value += str(res) + "\n}\n"
                else:
                    result += str(res) +',\n'
                    cur_value += str(res) +',\n'






def parse_text(text):
    lines = text.splitlines()
    global kol_bracket, constants
    global result, in_dict, cur_value, cur_name


    for num,line in enumerate(lines):
        line = line.strip()
        value = ""

        #пустая строка или комментарий
        if not line or line.startswith('/'):
            continue

        # словарь
        if line[0] == '}':
            if result[-2] == ",":
                 result = result[:-2] + '\n'
                 cur_value = cur_value[:-2] + '\n'
            result += kol_bracket * '  ' + "}\n"
            cur_value += (kol_bracket - 1)* '  ' + "}\n"

            parse_brackets(kol_bracket - 1, line, num)
            # неверная запись на ; всегда нужно завершать
            if not in_dict:
                if line[1] == ";":
                    result += "}\n"
                    constants[cur_name] = cur_value
                    cur_name = cur_value = ''
            if in_dict and line[1] != ";":
                raise SyntaxError(f"Неверный формат объявления константы: {line} (строка {num + 1})")
            value = line[1:]

        # выражение
        # while True:
        #     exp_match = re.search(r"\.[A-Z]+\.", line)
        #     if exp_match is None:
        #         break
        #
        #     expression = exp_match[0].strip('.')
        #     print(exp_match[0])
        #     res = calculating_constant(expression)
        #     if res is None:
        #         #Синтаксические ошибки выявляются с выдачей сообщений.
        #         raise ValueError(f"Неверное выражение: {expression} (строка {num + 1})")
        #     else:
        #          line = line.replace(exp_match[0], res)

        # обработка констант

        const_match = re.search("[A-Z]+",line)
        if const_match:
            name = const_match[0]


            # объявление константы
            if line.find("let") == 0:
                if (line[len(name) + 5] != "=" ) or in_dict or in_array:
                    raise SyntaxError(f"Неверный формат объявления константы: {line} (строка {num + 1})")

                if name in constants:
                    raise SyntaxError(f"Константа объявлена раннее: {line} (строка {num + 1})")

                cur_name = name
                result += "{\n" +  '  ' + f'"{name}": '
                value = line[(len(name) + 7):]

            # словарь
            if in_dict :
                line = line.strip().strip("\t")
                if line[len(name) + 1] != '=' : # or line[-1] != ';'
                    raise SyntaxError(f"Неверный формат элемента словаря: {line} (строка {num + 1})")
                value = line[len(name) + 3:]
                result += (kol_bracket+1) * '  ' + f'"{name}": '
                cur_value += kol_bracket*'  ' + f'"{name}": '

        # массив
        if in_array:
            print(value)
            values = value.split()
            for v in values:
                parse_value(v, line, num, name)
        else:
            parse_value(value, line, num, name)

    return result



def main():
    print("Введите текст на учебном конфигурационном языке:")
    text_input = sys.stdin.read() # or readlines
    # ctrl + D
    text_result = parse_text(text_input)

    if text_result:
        print("Результат на языке json:")
        sys.stdout.write(text_result)
    else:
        sys.stdout.write("Не удалось преобразовать исходный текст")

if __name__ == "__main__":
    main()
    # print("------------------------------")
    # print(constants)




'''
тест 1
let B = '( 6 7 );
let A = {
T = .B.;
};
let O = "tyt";
let T = {
P = 5;
};
let K = {
J = 0;
U = "sdfsd";
P = {
I = 9;
};
};
let Z = .K.;
'''
'''
let B: 5;
let K = ..6;
'''