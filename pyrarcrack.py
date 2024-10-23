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

# Argumentos da linha de comando
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
    '--only_printable',
    help='Only attempt combinations using printable characters',
    default=False,
    required=False,
)
parser.add_argument(
    '--unrar_path',
    help='Defines the path to the unrar executable, defaulting to the value from environment variables.',
    default='unrar',
    required=False,
)
parser.add_argument(
    '--unrar_lang',
    help='--unrar_lang LANG     Specifies the language for unrar messages, which is necessary to detect when an operation is successful. [eng/pt-br]',
    default='eng',
    required=False,
)
parser.add_argument('--file', help='.rar file [file.rar]', type=str)

args = parser.parse_args()

if args.only_printable:
    chars = printable


def format_string(string):
    """Formatar caracteres especiais."""
    formated = map(
        lambda char: char if char not in special_chars else f'\\{char}', string)
    return ''.join(formated)


def generate_combinations(alphabet, start, stop):
    """Gerar e testar combinações"""
    current_index = 0
    for length in range(start, stop + 1):
        current_index += 1
        for combination in product(alphabet, repeat=length):
            yield ''.join(combination), current_index


def try_password(combination, attempt_count, total_attempts):
    """Tentar uma combinação de senha para desbloquear o arquivo .rar."""
    formated_combination = format_string(combination)

    cmd = Popen(
        f'{args.unrar_path} t -p{formated_combination} {args.file}'.split(),
        stdout=PIPE,
        stderr=PIPE,
        creationflags=CREATE_NO_WINDOW,
    )
    out, err = cmd.communicate()

    if args.verbose and attempt_count % 100 == 0:
        print(f'Trying: {attempt_count}...{
              min(attempt_count+100, total_attempts)}/{total_attempts}')

    if args.unrar_lang == 'eng':
        ok_message = 'All OK'
    elif args.unrar_lang == 'pt-br':
        ok_message = 'Tudo OK'

    if ok_message in out.decode():
        return combination
    return False


if __name__ == '__main__':
    if not exists(args.file):
        raise FileNotFoundError(args.file)

    if args.stop < args.start:
        raise Exception('Stop number is less than start')

    # Calcular o número total de combinações
    total_attempts = sum(
        len(chars) ** length for length in range(args.start, args.stop + 1))

    start_time = time()
    attempt_count = 0
    # Multiprocessamento para testar combinações
    print("Started to generate and test combinations...")
    with Pool(cpu_count()) as pool:
        for combination, current_index in generate_combinations(args.alphabet, args.start, args.stop):
            result = pool.apply_async(
                try_password, (combination, attempt_count, total_attempts))
            attempt_count += 1

            if result.get():
                print(f'Password found: {result.get()}')
                print(f'Time: {time() - start_time}')
                sys.exit(0)
