#!/usr/bin/env python3
from typing import Tuple
from termcolor import colored
import struct
import sys
import argparse

def convert_str_to_int(v: str) -> int:
    if(v[0:2] == "0x"):
        return int(v, 16)
    else:
        return int(v)

def color1(list_bin: str) -> str:
    s = ""
    for b in list_bin:
        if b == "1":
            s += colored("1", 'red', attrs=['bold'])
        else:
            s += "0"
    return s

center_center = "┼"
bot_left_corner = "└"
bot = "─"
bot_mid_corner = "┴"
up_mid_corner = "┬"
bot_right_corner = "┘"
right_mid_corner = "┤"

char_sep = "│"
def binary_with_space(value: int, size: int=-1, highlight: Tuple[int, int]=(-1,-1)):
    svalue = bin(value)[2::]
    if(size != -1 and size > len(svalue)):
        svalue = "0" * (size - len(svalue)) + svalue
    elif(size == -1 and len(svalue) % 4 != 0):
        svalue = "0" * (4 - len(svalue) % 4) + svalue
    size = len(svalue)
    final = ""
    final_link = ""
    final_bit_nb = ""
    final_hex_nb = ""
    nb_sep_add = 0
    for i in range(0, len(svalue), 4):
        sep = " %s " % char_sep
        if(len(final) == 0):
            sep = ""
        else:
            nb_sep_add += 1
        final += sep + color1(svalue[i:i+4])
        final_link += '{0: >7}'.format(bot * 2 + up_mid_corner + bot * 3 + center_center)
        final_bit_nb += '{0: >7}'.format(char_sep + '{0: >4}'.format(str(len(svalue) - i - 4)))
        final_hex_nb += '{0: >3}'.format(hex(int(svalue[i:i+4], 2))[2:]) + " " * 4
    final =  char_sep + " " + final + " " + char_sep + "\n" + bot_left_corner + final_link[:-1] + right_mid_corner + "\n" + " "  + final_bit_nb + "\n" + " " + final_hex_nb
    print(final)

def int_with_space(value: int) -> str:
    s = str(value)
    final_s = ""
    for i in range(0, len(s)+3, 3):
        start = len(s)-(i+3)
        end = len(s)-i
        if(start < 0):
            start = 0
        if(end < 0):
            break
        final_s = s[start:end] + " " + final_s
    return final_s.strip()

def hex_with_space(value: int, bitsize: int) -> str:
    s = "0x%0{}x".format(bitsize/4) % value
    final_s = ""
    for i in range(0, len(s)+4, 4):
        start = len(s)-(i+4)
        end = len(s)-i
        if(start < 0):
            start = 0
        if(end < 0):
            break
        final_s = s[start:end] + " " + final_s
    return final_s.strip()

def to_float(value: int, bitsize: int) -> str:
    if(bitsize == 16):
        buff = struct.pack("H", value)
        return str(struct.unpack("e", buff)[0])
    elif(bitsize == 32):
        buff = struct.pack("I", value)
        return str(struct.unpack("f", buff)[0])
    elif(bitsize == 64):
        buff = struct.pack("Q", value)
        return str(struct.unpack("d", buff)[0])
    else:
        raise Exception("Bitsize issue")

def get_closer_bitsize(value: int) -> int:
    if(value < 0xFF):
        return 1 * 8
    elif(value < 0xFFFF):
        return 2 * 8
    elif(value < 0xFFFFFFFF):
        return 4 * 8
    elif(value < 0xFFFFFFFFFFFFFFFF):
        return 8 * 8
    else:
        raise Exception("value too high")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Nice display of integer", prog=sys.argv[0])
    parser.add_argument('number', type=str, help='Number to display')
    parser.add_argument("--bitsize", default=-1, type=int)
    args = parser.parse_args()
    return args

def main(args: argparse.Namespace):
    number = 0
    if(args.number[0:2].lower() == "0x"):
        number = int(args.number, 16)
    elif(args.number[0:2].lower() == "0b"):
        number = int(args.number, 2)
    else:
        number = int(args.number)

    bitsize = args.bitsize
    if(args.bitsize == -1):
        bitsize = get_closer_bitsize(number)
    binary_with_space(number, bitsize)
    print()
    hexa_number = hex_with_space(number, bitsize)
    print(colored("Hexa:", attrs=['underline']) + " " * (3 + 0) + ("{0: >%d}" % (32)).format(hexa_number))
    int_number = int_with_space(number)
    print(colored("Int:", attrs=['underline'])  + " " * (4 + 0) + ("{0: >%d}" % (32)).format(int_number))
    if(bitsize > 16):
        float_number = to_float(number, bitsize)
        print(colored("Float%02d:" % bitsize, attrs=['underline'])  + " " * (0 + 0) + ("{0: >%d}" % (32)).format(float_number))

if(__name__ == '__main__'):
    args = parse_args()
    main(args)

