import parser
import unittest


class IniParserUnitTests(unittest.TestCase):
    def setUp(self):
        self.p = parser.Parser()

    def test_is_comment(self):
        self.assertTrue(self.p.is_comment(";omar;;"), True)
        self.assertTrue(self.p.is_comment("#omar;;"), True)
        self.assertFalse(self.p.is_comment(""), False)
        self.assertFalse(
            self.p.is_comment(" ;"),
            False)  # must be passed uninteded
        self.assertFalse(self.p.is_comment("asd"), False)

    def test_is_section(self):
        self.assertTrue(self.p.is_section("[s]"))
        self.assertTrue(self.p.is_section("[s=sad]"))
        self.assertFalse(self.p.is_section(""))
        self.assertFalse(self.p.is_section(" [asd]"))

    def test_is_empty(self):
        self.assertTrue(self.p.is_empty(""))
        self.assertFalse(self.p.is_empty("a"))

    def test_parse_key(self):
        self.assertEqual(self.p.parse_key("mo = salah"), ["mo", "salah"])
        self.assertEqual(
            self.p.parse_key("asd = sda';dsak==a asd"), [
                "asd", "sda';dsak==a asd"])

    def test_add_entry(self):
        self.p.add_entry("sec1", "attr1", "val1")
        self.assertTrue(self.p.parseOutput.has_section("sec1"))
        self.assertEqual(
            self.p.parseOutput.get_property(
                "sec1", "attr1"), "val1")


if __name__ == "__main__":
    unittest.main()
