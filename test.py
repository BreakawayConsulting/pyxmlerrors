from pyxmlerrors import *
import unittest

class TestXml(unittest.TestCase):
    def test_xml_error(self):
        bad_xml = """<bad_xml>
  <this_element>is_wrong</this_element>
</bad_xml>"""

        dom = xml_parse_string(bad_xml, name="bad_xml")
        first_child = dom.getElementsByTagName('this_element')[0]
        self.assertEqual(xml_error_str(first_child, "msg"), "bad_xml:2.2 msg")

    def test_malformed_xml(self):
        bad_xml = """<bad_xml>
  <this_element>is_wrong
</bad_xml>"""
        try:
            dom = xml_parse_string(bad_xml, name="bad_xml", start_line=20)
        except ExpatError as e:
            self.assertEqual(e._path, "bad_xml")
            self.assertEqual(e.lineno, 23)
        else:
            self.fail("ExpatError not raised")

