"""
Copyright (c) 2013 Breakaway Consulting Pty. Ltd.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import xml.dom.minidom
import xml.dom.expatbuilder
from xml.parsers.expat import ExpatError

def monkey_start_element_handler(self, name, attributes):
    """This function is monkey-patched over the standard start_element_handle method.

    It adds the _line and _col attributes to the element node so that later error-checking can produce useful,
    targeted error messages.

    """
    real_start_element_handler(self, name, attributes)
    node = self.curNode
    node._line = self.getParser().CurrentLineNumber
    node._col = self.getParser().CurrentColumnNumber
real_start_element_handler = xml.dom.expatbuilder.ExpatBuilderNS.start_element_handler
xml.dom.expatbuilder.ExpatBuilderNS.start_element_handler = monkey_start_element_handler


def xml_error_str(el, msg):
    """Return an error string in the form:

    filename:lineno.colno msg

    """
    return "{}:{}.{} {}".format(el.ownerDocument._path, el.ownerDocument._start_line + el._line, el._col, msg)


def xml_parse_file(filename):
    """Parse XML file `filename` and return the documentElement.

    This is a thin-wrapper for the underlying standard file parsing routine that add extra attributes to the
    DOM to enable better diagnostics via the xml_error_str function.

    """
    try:
        dom = xml.dom.minidom.parse(filename)
    except ExpatError as e:
        e._path = filename
        raise e

    dom._path = filename
    dom._start_line = 0
    return dom


def xml_parse_string(string, name='<string>', start_line=0):
    """Parse an XML string.

    Optionally a name can be provided that will be used when providing diagnosics.
    In the case where the string has been extracted from another file the start_line parameter can be used to adjust
    the line number diagnostics.

    """
    try:
        dom = xml.dom.minidom.parseString(string)
    except ExpatError as e:
        e._path = name
        e.lineno += start_line
        raise e

    dom._path = name
    dom._start_line = start_line
    return dom
