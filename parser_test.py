import parser
import unittest
class IniParserTets(unittest.TestCase):
    def test_global_attrs(self):
        string = """

        o1 = omar
        o2 = omar
        o3 = omar
        hey = hi
        th = th
        """
        result = parser.parseIni(string)
        self.assertEqual(result.getGlobalProperty("o1"), "omar")
        self.assertEqual(result.getGlobalProperty("o2"), "omar")
        self.assertEqual(result.getGlobalProperty("o3"), "omar")
        self.assertEqual(result.getGlobalProperty("hey"), "hi")
        self.assertEqual(result.getGlobalProperty("th"), "th")
        self.assertEqual(result.getGlobalProperty("TH"), "th") # ini file is case insensitive
    def test_section(self):
        string = """
        [intern]
            company = codescalers
            period = 2 months
            date = 1/2/3
        [python]
            author = 7mada
            implementer = 7mada
        """
        result = parser.parseIni(string)
        self.assertEqual(result.getProperty("intern", "company"), "codescalers")
        self.assertEqual(result.getProperty("intern", "date"), "1/2/3")
        self.assertEqual(result.getProperty("python", "author"), "7mada")
    def test_special_char(self):
        string = """
        [section]
            attr1 = om=-12/xcz,pase2;
            attr2 = attr3 = attr4 = 0
        """
        result = parser.parseIni(string)
        self.assertEqual(result.getProperty("section", "attr1"), "om=-12/xcz,pase2;")
        self.assertEqual(result.getProperty("section", "attr2"), "attr3 = attr4 = 0")
    def test_empty_lines(self):
        string = """
        [section]

            attr1 = 1

    attr2 = 2

    [section2]
        attr2 = 4
        """
        result = parser.parseIni(string)
        self.assertEqual(result.getProperty("section", "attr1"), "1")
        self.assertEqual(result.getProperty("section", "attr2"), "2")
        self.assertEqual(result.getProperty("section2", "attr2"), "4")
    def test_collisioning_names_in_different_sections(self):
        string = """
        attr = 0
        [section1]
            attr = 1
        [section2]
            attr = 2
        """
        result = parser.parseIni(string)
        self.assertEqual(result.getGlobalProperty("attr"), "0")
        self.assertEqual(result.getProperty("section1", "attr"), "1")
        self.assertEqual(result.getProperty("section2", "attr"), "2")
    def test_comments(self):
        string = """
        #this is the first section
        [section1]
            attr = 1
        ;this is the second section
        [section2]
            attr = 1
        """
        result = parser.parseIni(string) #not producing errors is good enough

if __name__ == "__main__":
    unittest.main()
