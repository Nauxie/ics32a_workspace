# project0b_sanitycheck.py
#
# ICS 32A Fall 2017
# Project #0B: Square One
#
# This is a sanity checker for your Project #0B solution, which checks whether
# your solution meets the basic requirements:
#
# * The file is named correctly
# * It's possible to run the program by executing the module
# * Your program generates the correct output for one scenario (the example
#   shown in the project write-up)
#
# There are other tests you'll want to run besides the one scenario here,
# because we'll be testing more than just one when we grade your work, but if
# your program is unable to pass this sanity checker, it will certainly be
# unable to pass our automated tests.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THIS CODE, though you can certainly
# feel free to take a look at it.


import collections
import pathlib
import queue
import sys
import subprocess
import threading
import time
import traceback
import typing



class TextProcessReadTimeout(Exception):
    pass



class TextProcess:
    _READ_INTERVAL_IN_SECONDS = 0.025


    def __init__(self, args: [str], working_directory: str):
        self._process = subprocess.Popen(
            args, cwd = working_directory, bufsize = 0,
            stdin = subprocess.PIPE, stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)

        self._stdout_read_trigger = queue.Queue()
        self._stdout_buffer = queue.Queue()

        self._stdout_thread = threading.Thread(
            target = self._stdout_read_loop, daemon = True)

        self._stdout_thread.start()


    def __enter__(self):
        return self


    def __exit__(self, tr, exc, val):
        self.close()


    def close(self):
        self._stdout_read_trigger.put('stop')
        self._process.terminate()
        self._process.wait()
        self._process.stdout.close()
        self._process.stdin.close()


    def write_line(self, line: str) -> None:
        try:
            self._process.stdin.write((line + '\n').encode(encoding = 'utf-8'))
            self._process.stdin.flush()

        except OSError:
            pass


    def read_line(self, timeout: float = None) -> str or None:
        self._stdout_read_trigger.put('read')
        
        sleep_time = 0
        
        while timeout == None or sleep_time < timeout:
            try:
                next_result = self._stdout_buffer.get_nowait()

                if next_result == None:
                    return None
                elif isinstance(next_result, Exception):
                    raise next_result
                else:
                    return next_result.decode(encoding = 'utf-8')

            except queue.Empty:
                time.sleep(TextProcess._READ_INTERVAL_IN_SECONDS)
                sleep_time += TextProcess._READ_INTERVAL_IN_SECONDS

        raise TextProcessReadTimeout()


    def _stdout_read_loop(self):
        try:
            while self._process.returncode == None:
                if self._stdout_read_trigger.get() == 'read':
                    line = self._process.stdout.readline()

                    if line == b'':
                        self._stdout_buffer.put(None)
                    else:
                        self._stdout_buffer.put(line)
                else:
                    break

        except Exception as e:
            self._stdout_buffer.put(e)



class TestFailure(Exception):
    pass



class TestInputLine:
    def __init__(self, text: str):
        self._text = text

    
    def execute(self, process: TextProcess) -> None:
        try:
            process.write_line(self._text)

        except Exception as e:
            print_labeled_output(
                'EXCEPTION',
                [tb_line.rstrip() for tb_line in traceback.format_exc().split('\n')])

            raise TestFailure()

        print_labeled_output('INPUT', self._text)



class TestOutputLine:
    def __init__(self, text: str, timeout_in_seconds: float):
        self._text = text
        self._timeout_in_seconds = timeout_in_seconds


    def execute(self, process: TextProcess) -> None:
        try:
            output_line = process.read_line(self._timeout_in_seconds)

        except TextProcessReadTimeout:
            output_line = None

        except Exception as e:
            print_labeled_output(
                'EXCEPTION',
                [tb_line.rstrip() for tb_line in traceback.format_exc().split('\n')])

            raise TestFailure()

        if output_line != None:
            if output_line.endswith('\r\n'):
                output_line = output_line[:-2]
            elif output_line.endswith('\n'):
                output_line = output_line[:-1]

            print_labeled_output('OUTPUT', output_line)

            if output_line != self._text:
                print_labeled_output('EXPECTED', self._text)

                index = min(len(output_line), len(self._text))

                for i in range(min(len(output_line), len(self._text))):
                    if output_line[i] != self._text[i]:
                        index = i
                        break

                print_labeled_output('', (' ' * index) + '^')

                print_labeled_output(
                    'ERROR',
                    'This line of output did not match what was expected.  The first',
                    'incorrect character is marked with a ^ above.',
                    '(If you don\'t see a difference, perhaps your program printed',
                    'extra whitespace on the end of this line.)')

                raise TestFailure()

        else:
            print_labeled_output('EXPECTED', self._text)

            print_labeled_output(
                'ERROR',
                'This line of output was expected, but the program did not generate',
                'any additional output after waiting for {} second(s).'.format(self._timeout_in_seconds))

            raise TestFailure()



class TestEndOfOutput:
    def __init__(self, timeout_in_seconds: float):
        self._timeout_in_seconds = timeout_in_seconds


    def execute(self, process: TextProcess) -> None:
        output_line = process.read_line(self._timeout_in_seconds)

        if output_line != None:
            print_labeled_output('OUTPUT', output_line)

            print_labeled_output(
                'ERROR',
                'Extra output was printed after the program should not have generated',
                'any additional output')

            raise TestFailure()



TEST_LINES = [
    TestInputLine('4'),
    TestOutputLine('+-+', 1.0),
    TestOutputLine('| |', 0.1),
    TestOutputLine('+-+-+', 0.1),
    TestOutputLine('  | |', 0.1),
    TestOutputLine('  +-+-+', 0.1),
    TestOutputLine('    | |', 0.1),
    TestOutputLine('    +-+-+', 0.1),
    TestOutputLine('      | |', 0.1),
    TestOutputLine('      +-+', 0.1),
    TestEndOfOutput(1.0)
]



def run_test() -> None:
    process = None

    try:
        process = start_process()
        run_test_lines(process)
        print_labeled_output(
            'PASSED',
            'Your "project0b.py" passed the sanity checker.  Note that there are',
            'other tests you\'ll want to run on your own, because we\'ll be testing',
            'scenarios other than just this one.  But you\'re well on your way to',
            'being done with Project #0B.')

    except TestFailure:
        print_labeled_output(
            'FAILED',
            'The sanity checker has failed, for the reasons described above.')

    finally:
        if process != None:
            process.close()



def start_process() -> TextProcess:
    filenames_in_dir = [p.name for p in list(pathlib.Path.cwd().iterdir()) if p.is_file()]

    if not 'project0b.py' in filenames_in_dir:
        print_labeled_output(
            'ERROR',
            'Cannot find file "project0b.py" in this directory.',
            'Make sure that the sanity checker is in the same directory as the',
            '"project0b.py" that comprises your Project #0B solution.  Also, be',
            'sure that you\'ve named your "project0b.py" file correctly, noting',
            'that capitalization and spacing matter.')

        raise TestFailure()

    else:
        return TextProcess(
            [sys.executable, str(pathlib.Path.cwd() / 'project0b.py')],
            str(pathlib.Path.cwd()))



def print_labeled_output(label: str, *msg_lines: typing.Iterable[str]) -> None:
    showed_first = False

    for msg_line in msg_lines:
        if not showed_first:
            print('{:10}|{}'.format(label, msg_line))
            showed_first = True
        else:
            print('{:10}|{}'.format(' ', msg_line))

    if not showed_first:
        print(label)



def run_test_lines(process: TextProcess) -> None:
    for line in TEST_LINES:
        line.execute(process)



if __name__ == '__main__':
    run_test()

