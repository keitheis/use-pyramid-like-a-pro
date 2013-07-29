import re

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


LINE_PARTS_RE = re.compile('(?P<indent>\s*)(?P<line>.*)\s*')


def code(context, language_name, code_block,
         indent_spaces=4,
         default_indent='',
         line_numbers=False,
         css_class="codehilite"):
    lexer = get_lexer_by_name(language_name)
    formatter = CodeHtmlFormatter(linenos=line_numbers,
                                  indentspaces=indent_spaces,
                                  cssclass=css_class)
    formatter.levelspaces = indent_spaces
    formatter.defaultindent = default_indent
    result = highlight(code_block, lexer, formatter)
    #print(">>> code_block >>>")
    #print(code_block)
    #print(">>> end code_block >>>")
    #print(result)
    ##print(_indent_spaces(result))
    return result


class CodeHtmlFormatter(HtmlFormatter):

    defaultindent = ''
    levelspaces = 4
    _first_indent_level = None
    _first_diff_spaces = None

    def wrap(self, source, outfile):
        self._first_indent_level = None
        self._first_diff_spaces = None
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<div class="{}">'.format(self.cssclass)
        default_indent = self.defaultindent
        for i, line in source:
            if i == 1:
                level, line = _get_indent_level(line)
                spaces = ''
                if self._first_indent_level is None:
                    self._first_indent_level = level
                elif level > self._first_indent_level:
                    if (self._first_diff_spaces is None):
                        self._first_diff_spaces = (
                            level - self._first_indent_level)
                    diff_spaces = level - self._first_indent_level
                    extra_spaces = diff_spaces % self._first_diff_spaces
                    diff_levels = diff_spaces / self._first_diff_spaces
                    spaces = '&nbsp;' * (self.levelspaces * diff_levels
                                         + extra_spaces)
                # it's a line of formatted code
                line = default_indent + spaces + line + '<br/>'
                #print line
            yield i, line
        yield 0, '</div>'


def _get_indent_level(line):
    match = LINE_PARTS_RE.match(line)
    return len(match.group('indent')), match.group('line')
