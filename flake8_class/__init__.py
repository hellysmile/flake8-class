import tokenize
from itertools import groupby

import pep8

from flake8_class.__about__ import __version__


class ClassException(Exception):
    pass


class ClassChecker(object):
    name = __name__
    version = __version__

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
        for error in self._get_class_errors(file_contents):
            start_row, start_col = error

            yield {
                'message': 'C000 Fix class declaration.',
                'line': start_row,
                'col': start_col,
            }

    def _get_class_errors(self, file_contents):
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

            while True:
                try:
                    token = next(gen)
                except StopIteration:
                    raise NotImplementedError
                else:
                    scope.append(token)

                    if token.string == ':':
                        break

            code = [el.string for el in scope][2:-1]

            if not code:
                continue

            assert code[0] == '('
            assert code[-1] == ')'

            code = code[1:-1]

            if not code:
                continue

            if '\n' != code[0]:
                yield start_row, start_col
                continue

            separator = ','

            parents = [list(y) for x, y in groupby(code, lambda z: z == separator) if not x]

            for parent in parents:
                if '\n' != parent[0]:
                    yield start_row, start_col
                    continue

            ending = parents[-1]

            if '\n' != ending[-1]:
                yield start_row, start_col
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
