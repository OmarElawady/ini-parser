import parser
import unittest
class IniParserUnitTests(unittest.TestCase):
    def setUp(self):
        self.p = parser.Parser()
    def test_is_comment(self):
        self.assertTrue(self.p.is_comment(";omar;;"), True) 
        self.assertTrue(self.p.is_comment("#omar;;"), True) 
        self.assertFalse(self.p.is_comment(""), False)
        self.assertFalse(self.p.is_comment(" ;"), False) # must be passed uninteded
        self.assertFalse(self.p.is_comment("asd"), False)
    def test_is_section(self):
        self.assertTrue(self.p.is_section("[s]"))
        self.assertTrue(self.p.is_section("[s=sad]"))
        self.assertFalse(self.p.is_section(""))
        self.assertFalse(self.p.is_section(" [asd]"))
    def test_is_empty(self):
        self.assertTrue(self.p.is_empty(""))
        self.assertFalse(self.p.is_empty("a"))
    def test_parseKey(self):
        self.assertEquals(self.p.parseKey("mo = salah"), ["mo", "salah"])
        self.assertEquals(self.p.parseKey("asd = sda';dsak==a asd"), ["asd", "sda';dsak==a asd"])
    def test_addEntry(self):
        self.p.addEntry("sec1", "attr1", "val1")
        self.assertTrue(self.p.parseOutput.hasSection("sec1"))
        self.assertEqual(self.p.parseOutput.getProperty("sec1", "attr1"), "val1")
if __name__ == "__main__":
    unittest.main()
