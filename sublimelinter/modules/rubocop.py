import re

from .base_linter import BaseLinter, INPUT_METHOD_TEMP_FILE

CONFIG = {
    'language': 'rubocop',
    'executable': 'rubocop',
    'lint_args': "{filename}",
    'input_method': INPUT_METHOD_TEMP_FILE
}


class Linter(BaseLinter):

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        for line in errors.splitlines():
            match = re.match(r'^(?P<file>[\w.\\\/-]+):(?P<line>\d+):(?P<column>\d+):\s?(?P<type>[WEC]):\s?(?P<error>.*)', line)

            if match:
                error_type = match.group('type')
                error = match.group('error')
                line = int(match.group('line'))
                column = int(match.group('column')) - 1

                if error_type == 'W' or error_type == 'C':
                    messages = warningMessages
                    underlines = warningUnderlines
                else:
                    messages = errorMessages
                    underlines = errorUnderlines

                self.add_message(line, lines, error, messages)
                self.underline_range(view, line, column, underlines)
