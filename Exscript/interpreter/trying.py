#
# Copyright (C) 2010-2017 Samuel Abels
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import print_function, absolute_import
import Exscript.interpreter.code
from ..protocols.exception import ProtocolException
from .scope import Scope


class Try(Scope):

    def __init__(self, lexer, parser, parent):
        Scope.__init__(self, 'Try', lexer, parser, parent)

        lexer.next_if('whitespace')
        lexer.expect(self, 'keyword', 'try')
        lexer.skip(['whitespace', 'newline'])
        self.block = Exscript.interpreter.code.Code(lexer, parser, parent)

    def value(self, context):
        try:
            self.block.value(context)
        except ProtocolException as e:
            return 1
        return 1

    def dump(self, indent=0):
        print((' ' * indent) + self.name, 'start')
        self.block.dump(indent + 1)
        print((' ' * indent) + self.name, 'end')
