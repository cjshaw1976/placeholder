"""
Custom path converters for urls
https://docs.djangoproject.com/en/dev/topics/http/urls/#registering-custom-path-converters
"""


# Match a hexcolor in the url.
# Must start with a # and contain 3 or 6 hexidecimal characters (0-9 and A-F),
# in either lower or upper case.
class HexColorConverter:
    regex = '([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


# File Formats to Return
class FileFormatConverter:
    regex = '([b:B][m:M][p:P]|[g:G][i:I][f:F]|[j:J][p:P][e:E]?[g:G]|[p:P][c:C][x:X]|[p:P][n:N][g:G])'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


# Limit width min 1, max 1920
class MaxWidthConverter:
    regex = '([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|1[0-8][0-9][0-9]|19[0-1][0-9]|1920)'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value


# Limit height min 1, max 1080
class MaxHeightConverter:
    regex = '([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|10[0-7][0-9]|1080)'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value
