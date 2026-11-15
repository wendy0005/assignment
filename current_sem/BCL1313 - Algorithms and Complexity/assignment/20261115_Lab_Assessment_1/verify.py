"""Build the submission and capture repeatable, real execution evidence."""
from pathlib import Path
import argparse
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--sanitize', action='store_true')
args = parser.parse_args()
(ROOT / 'build').mkdir(exist_ok=True)
(ROOT / 'evidence').mkdir(exist_ok=True)
flags = ['-std=c++17', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
if args.sanitize:
    flags += ['-fsanitize=address,undefined', '-g']
for source, output in [('restaurant_orders.cpp', 'restaurant_orders'),
                       ('test_restaurant.cpp', 'test_restaurant')]:
    subprocess.run(['g++', *flags, source, '-o', f'build/{output}'],
                   cwd=ROOT, check=True)

def execute(binary, arguments=(), user_input=None):
    result = subprocess.run([str(ROOT / 'build' / binary), *arguments],
                            input=user_input, capture_output=True, text=True,
                            check=True)
    assert not result.stderr, result.stderr
    return result.stdout

demo = execute('restaurant_orders', ['--demo'])
tests = execute('test_restaurant')
(ROOT / 'evidence/demo_output.txt').write_text(demo)
(ROOT / 'evidence/tests_output.txt').write_text(tests)
menu_input = ('x\n2abc\n9\n2\n3\n4\n5\n6\n7\n1\n  \nAiman\nChicken Rice\n'
              '0\n-1\n1.5\n2abc\n2\n3\n4\n2\n5\n7\n6\n7\n0\n')
menu = execute('restaurant_orders', user_input=menu_input)
for expected in ['Invalid choice.', 'Invalid quantity.',
                 'Queue is empty. No order processed.',
                 'Stack is empty. No order popped.', 'Enqueued ORD001',
                 'Processed ORD001 -> automatically pushed ORD001',
                 'Popped ORD001', 'Session ended.']:
    assert expected in menu, expected
assert menu.count('Enqueued ORD001') == 1
(ROOT / 'evidence/interactive_output.txt').write_text(menu)
commands = []
for i in range(11):
    commands += ['1', f'Customer{i}', 'Rice', '1']
commands += ['4', '0']
overflow = execute('restaurant_orders', user_input='\n'.join(commands) + '\n')
assert 'Queue is full. Order was not added.' in overflow
assert 'count = 10' in overflow and 'Enqueued ORD011' not in overflow
(ROOT / 'evidence/interactive_full_queue.txt').write_text(overflow)
eof = execute('restaurant_orders', user_input='1\nAiman\n')
assert 'Enqueued' not in eof
bad = subprocess.run([str(ROOT / 'build/restaurant_orders'), '--unknown'],
                     capture_output=True, text=True)
assert bad.returncode == 1 and 'Usage:' in bad.stderr
summary = (tests +
    'PASS 8: Interactive menu, invalid choices and quantities, empty operations.\n'
    'PASS 9: Interactive full queue rejects eleventh order without overwriting data.\n'
    'PASS 10: Input EOF creates no partial order; invalid command option returns error.\n'
    'All ten validation groups passed.\n')
if args.sanitize:
    summary += 'Address and undefined behaviour sanitizers reported no errors.\n'
(ROOT / 'evidence/validation_output.txt').write_text(summary)
print(summary)
