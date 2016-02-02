from context import Context

__author__ = 'Peter Vrba <phonkee@phonkee.eu>'

# fetch version from package VERSION file
__VERSION__ = open('../VERSION', 'r').read().strip()

__all__ = [
    'Context',
    '__VERSION__'
]
