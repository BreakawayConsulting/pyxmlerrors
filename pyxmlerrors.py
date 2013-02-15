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
