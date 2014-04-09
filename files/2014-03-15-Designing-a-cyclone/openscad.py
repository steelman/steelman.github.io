from pygments.lexer import RegexLexer,include
from pygments.token import *

__all__ = [ 'OpenSCADLexer',]

class OpenSCADLexer(RegexLexer):
        """
        Lexer for OpenSCAD files.
        """

        name = 'OpenSCAD'
        aliases = ['openscad', 'scad']
        filenames = ['*.scad']

        tokens = {
            # CFamilyLexer
            'whitespace': [
                (r'\n', Text),
                (r'\s+', Text),
                (r'//(\n|(.|\n)*?[^\\]\n)', Comment.Single),
                (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment.Multiline),
                ],
            'string': [
                (r'"', String, '#pop'),
                (r'\\[rnt"]',String.Escape),
                (r'[^"]+', String),
                ],
            'name': [
                (r'[A-Za-z0-9_]+', Name)
                ],
            'numbers': [
                (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
                (r'\d+[eE][+-]?[0-9]+j?', Number.Float),
                (r'\d+', Number.Integer),
                ],
            'builtins': [
                # tokentypes["math"]
                (r'abs|sign|acos|asin|atan|atan2|sin|cos|floor|round|ceil|ln|'
                 r'log|lookup|min|max|pow|sqrt|exp|rands', Name.Builtin),
                #tokentypes['csgop']
                (r'union|intersection|difference|render', Name.Builtin),
                #tokentypes['transform']
                (r'scale|translate|rotate|multmatrix|color|projection|hull|'
                 r'resize|mirror|minkowski', Name.Builtin),
                # tokentypes['prim3d']
                (r'cube|cylinder|sphere|polyhedron', Name.Builtin),
                #tokentypes['prim2d']
                (r'square|polygon|circle', Name.Builtin),
                #tokentypes['special']
                (r'child|\$(children|children|fn|fa|fs|t|vpt|vpr)',
                 Name.Builtin.Pseudo),
                #tokentypes['extrude']
                (r'linear_extrude|rotate_extrude', Name.Builtin),
                #tokentypes['import']
                (r'include|use|import_stl|import|import_dxf|dxf_dim|dxf_cross|'
                 r'surface', Name.Builtin),
                ],
            'root': [
                include('numbers'),
                include('whitespace'),
                (r'"', String, 'string'),
                (r'[]{}:(),;[]', Punctuation),
                #tokentypes['operator']
                (r'=|!|&&|\|\||\+|-|\*|/|%|!|#|;', Operator),
                #tokentypes["keyword"]
                (r'module|function|for|intersection_for|if|assign|echo|search|str',
                 Keyword),
                (r'true|false', Keyword.Constant),
                include('builtins'),
                include('name'),
                ]}

"""

        builtin global variables

        tokentypes['bracket']
        << '[' << ']' << '(' << ')';
        tokentypes['curlies']
        << '{' << '}';
open("foo",1)
"""
