When dealing with XML provided by a user, it is nice to be able to provide targeted error messages.

This small library provides 3 functions: `xml_parse_file`, `xml_parse_string` and `xml_error_str`.
To use it simply call `xml_parse_file` in places you would otherwise call `xml.minidom.parse`, and `xml_parse_string` in place of `xml.minidom.parseString`.
When you want to report an error to the user call `xml_error_str` passing element that is problematic.

Checkout `test.py` for some usage examples.

Feel free to take `pyxmlerrors.py` and simply drop it in to your project.

