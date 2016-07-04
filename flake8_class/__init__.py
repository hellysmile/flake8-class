import re
import tokenize
from collections import Counter
from lib2to3 import pytree
from lib2to3.pgen2.driver import Driver
from lib2to3.pygram import python_grammar

try:
    import pycodestyle as pep8
except ImportError:
    import pep8

from flake8_class.__about__ import __version__


_driver = Driver(
    grammar=python_grammar,
    convert=pytree.convert,
)


class ClassChecker(object):
    name = __name__
    version = __version__

    def C000(self, start_row, start_col):  # noqa
        return {
            'message': self.C000.message,
            'line': start_row,
            'col': start_col,
        }
    C000.message = 'C000 Fix class declaration.'

    def __init__(self, tree, filename='(none)', builtins=None):
        self.filename = filename

    def get_file_contents(self):
        if self.filename in ('stdin', '-', None):
            return pep8.stdin_get_value().splitlines(True)
        else:
            return pep8.readlines(self.filename)

    def run(self):
        file_contents = self.get_file_contents()

        noqa_line_numbers = self.get_noqa_lines(file_contents)
        errors = self.get_class_errors(file_contents)

        for error in errors:
            if error.get('line') not in noqa_line_numbers:
                yield (error.get('line'), error.get('col'), error.get('message'), type(self))

    def get_noqa_lines(self, file_contents):
        tokens = [Token(t) for t in tokenize.generate_tokens(lambda L=iter(file_contents): next(L))]
        return [token.start_row
                for token in tokens
                if token.type == tokenize.COMMENT and token.string.endswith('noqa')]

    def get_class_errors(self, file_contents):
        tokens = [Token(t) for t in tokenize.generate_tokens(lambda L=iter(file_contents): next(L))]

        gen = iter(tokens)

        while True:
            try:
                token = next(gen)
            except StopIteration:
                break

            if token.type != tokenize.NAME:
                # ignore non names
                continue

            if token.string != 'class':
                # ignore non class declaration
                continue

            scope = [token]

            start_row, start_col = token.start

            last_colon = False

            while True:
                try:
                    token = next(gen)
                except StopIteration:
                    raise NotImplementedError
                else:
                    if last_colon:
                        if token.type == tokenize.NEWLINE:
                            break

                    scope.append(token)

                    if token.string == ':':
                        last_colon = True
                    else:
                        last_colon = False

            scope = scope[2:-1]

            if not scope:
                continue

            code = [el.string for el in scope]

            assert code[0] == '('
            assert code[-1] == ')'

            code = code[1:-1]
            scope = scope[1:-1]

            if not code:
                continue

            if '\n' != code[0]:
                yield self.C000(start_row, start_col)
                continue

            nls = Counter(code)['\n']

            source = ''.join(code).replace('\n', ',')

            source = re.sub(r'\,{2}', ',', source)

            if source[0] == ',':
                source = ''.join(source.split()[1:])

            source = '\nclass CLS(' + source + '):pass\n'

            tree = _driver.parse_string(source)

            nodes = len(tree.children[0].children[3].children)

            if nodes != 0:
                if nodes != nls:
                    yield self.C000(start_row, start_col)
                    continue


class Token:
    '''Python 2 and 3 compatible token'''
    def __init__(self, token):
        self.token = token

    @property
    def type(self):
        return self.token[0]

    @property
    def string(self):
        return self.token[1]

    @property
    def start(self):
        return self.token[2]

    @property
    def start_row(self):
        return self.token[2][0]

    @property
    def start_col(self):
        return self.token[2][1]
