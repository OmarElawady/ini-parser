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
        result = parser.parse_ini(string)
        self.assertEqual(result.get_global_property("o1"), "omar")
        self.assertEqual(result.get_global_property("o2"), "omar")
        self.assertEqual(result.get_global_property("o3"), "omar")
        self.assertEqual(result.get_global_property("hey"), "hi")
        self.assertEqual(result.get_global_property("th"), "th")
        self.assertEqual(
            result.get_global_property("TH"),
            "th")  # ini file is case insensitive

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
        result = parser.parse_ini(string)
        self.assertEqual(
            result.get_property(
                "intern",
                "company"),
            "codescalers")
        self.assertEqual(result.get_property("intern", "date"), "1/2/3")
        self.assertEqual(result.get_property("python", "author"), "7mada")

    def test_special_char(self):
        string = """
        [section]
            attr1 = om=-12/xcz,pase2;
            attr2 = attr3 = attr4 = 0
        """
        result = parser.parse_ini(string)
        self.assertEqual(
            result.get_property(
                "section",
                "attr1"),
            "om=-12/xcz,pase2;")
        self.assertEqual(
            result.get_property(
                "section",
                "attr2"),
            "attr3 = attr4 = 0")

    def test_empty_lines(self):
        string = """
        [section]

            attr1 = 1

    attr2 = 2

    [section2]
        attr2 = 4
        """
        result = parser.parse_ini(string)
        self.assertEqual(result.get_property("section", "attr1"), "1")
        self.assertEqual(result.get_property("section", "attr2"), "2")
        self.assertEqual(result.get_property("section2", "attr2"), "4")

    def test_collisioning_names_in_different_sections(self):
        string = """
        attr = 0
        [section1]
            attr = 1
        [section2]
            attr = 2
        """
        result = parser.parse_ini(string)
        self.assertEqual(result.get_global_property("attr"), "0")
        self.assertEqual(result.get_property("section1", "attr"), "1")
        self.assertEqual(result.get_property("section2", "attr"), "2")

    def test_comments(self):
        string = """
        #this is the first section
        [section1]
            attr = 1
        ;this is the second section
        [section2]
            attr = 1
        """
        parser.parse_ini(string)  # not producing errors is good enough


if __name__ == "__main__":
    unittest.main()
