"""
Bruteforce attack for .rar using unrar.

V: 0.0.2.4

Based on:
http://stackoverflow.com/questions/11747254/python-brute-force-algorithm
http://www.enigmagroup.org/code/view/python/168-Rar-password-cracker
http://rarcrack.sourceforge.net/
"""
from argparse import ArgumentParser
from itertools import product
from os.path import exists
from subprocess import PIPE, Popen, CREATE_NO_WINDOW
from multiprocessing import Pool, cpu_count
from string import printable
from time import time
import sys

chars = (
    printable
    + 'ÁáÂâàÀÃãÅåÄäÆæÉéÊêÈèËëÐðÍíÎîÌìÏïÓóÒòÔôØøÕõÖöÚúÛûÙùÜüÇçÑñÝý®©Þþß'
)
special_chars = "();<>`|~\"&\'}]"

parser = ArgumentParser(description='Python combination generator to unrar')

parser.add_argument(
    '--start',
    help='Number of characters of the initial string [1 -> "a", 2 -> "aa"]',
    type=int,
)

parser.add_argument(
    '--stop',
    help='Number of characters of the final string [3 -> "ßßß"]',
    type=int,
)

parser.add_argument(
    '--verbose', help='Show combintations', default=False, required=False
)

parser.add_argument(
    '--alphabet',
    help='Alternative chars to combinations',
    default=chars,
    required=False,
)

parser.add_argument(
    '--unrar_path',
    help='Define the path to unrar',
    default='unrar',
    required=False,
)

parser.add_argument('--file', help='.rar file [file.rar]', type=str)

args = parser.parse_args()

def format_string(string):
    """Formatar caracteres especiais."""
    formated = map(
        lambda char: char if char not in special_chars else f'\\{char}', string)
    return ''.join(formated)


def generate_combinations(alphabet, start, stop):
    """Gerar e testar combinações"""
    for length in range(start, stop + 1):
        for combination in product(alphabet, repeat=length):
            yield ''.join(combination)


def try_password(combination,z,v,b):
    """Tentar uma combinação de senha para desbloquear o arquivo .rar."""
    formated_combination = format_string(combination)

    cmd = Popen(
        f'{args.unrar_path} t -p{formated_combination} {args.file}'.split(),
        stdout=PIPE,
        stderr=PIPE,
        creationflags=CREATE_NO_WINDOW,
    )
    out, err = cmd.communicate()

    if 'All OK' in out.decode():
        return combination
    return False


if __name__ == '__main__':
    if not exists(args.file):
        raise FileNotFoundError(args.file)

    if args.stop < args.start:
        raise Exception('Stop number is less than start')

    start_time = time()
    # Multiprocessamento para testar combinações
    print("Started to generate and test combinations...")
    with Pool(cpu_count()) as pool:
        for combination in generate_combinations(args.alphabet, args.start, args.stop):
            result = pool.apply_async(
                try_password, (combination))

            if result.get():
                print(f'Password found: {result.get()}')
                print(f'Time: {time() - start_time}')
                sys.exit(0)
