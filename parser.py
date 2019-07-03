class ConfigData:
    """Data structure to store the result of the ini parsing."""

    def __init__(self):
        """Base for ConfigData

        data: dict of dicts to store the sections
        """
        self.data = {}

    def set_property(self, section, key, val):
        """Sets a new property within the given section.

        Arguments:
            section {str} -- the name of the section
            key     {str} -- the name of the key
            val     {str} -- the value associated with the key
        """
        section = section.lower()
        key = key.lower()
        val = val.lower()
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = val

    def has_section(self, section):
        """Checks whether the data contains the given section.

        Arguments:
            section {str} -- the name of the section

        Returns:
            bool -- true if the section exists
        """
        section = section.lower()
        return section in self.data

    def get_property(self, section, key):
        """Gets the value in the given section associated with key.

        Arguments:
            section {str} -- the name of the section
            key     {str} -- the key

        Raises:
            KeyError if section doesn't exist or key doesn't exist in section

        Returns:
            str -- ConfigData[section][key]
        """
        section = section.lower()
        key = key.lower()
        return self.data[section][key]

    def __len__(self):
        """Finds the number of section currently stored.

        Returns:
            int -- the number of sections
        """
        return len(
            list(
                filter(
                    lambda x: isinstance(
                        x,
                        dict),
                    self.data.values())))

    def has_property(self, section, key):
        """Checks whether there key exists in the given section.

        Arguments:
            section {str} -- the name of the section
            key     {str} -- the name of the key

        Returns:
            bool -- True if ConfigData[section][key] exists
        """
        section = section.lower()
        key = key.lower()
        return section in self.data and key in self.data[section]

    def get_section(self, section):
        """Extracts the data in the section.

        Arguments:
            section {str} -- the name of the section

        Raises:
            KeyError -- when the section doesn't exist

        Returns:
            dict -- the key value map of the passed section
        """
        section = section.lower()
        return self.data[section]

    def delete_property(self, section, key):
        """Deletes the given key in the given section.

        Arguments:
            section {str} -- the name of the section
            key     {str} -- the name of the key

        Raises:
            KeyError -- if the section or the key in the section doesn't exist
        """
        section = section.lower()
        key = key.lower()
        del self.data[section][key]

    def get_global_property(self, key):
        """Extracts the global value associated with the given key.

        Arguments:
            ket {str} -- the key of the global property

        Raises:
            KeyError -- if the key doesn't exist

        Returns:
            str -- the value of the property
        """
        key = key.lower()
        return self.data[key]

    def set_global_property(self, key, val):
        """Sets the value associated with the passed key to val.

        Arguments:
            key {str} -- the key of the global property
            val {str} -- the value to be stored

        Raises:
            KeyError -- if the key doesn't exist
        """
        key = key.lower()
        val = val.lower()
        self.data[key] = val

    def __str__(self):
        """Extracts a printable representation of the config data.

        Returns:
            str -- a string in the for of dict of dicts
        """
        return str(self.data)


class Parser:
    def __init__(self):
        """Base for parser.

        parseOutput: The value to which the parse output will be stored
        """
        self.parseOutput = ConfigData()

    def parse(self, string):
        """Parses the given string in the ini format.

        Arguments:
            string {str} -- a string representing the ini file in its format

        Raises:
            Exception -- if it reads a line which can't be processes \
                    (not a comment, key=value nor [section])

        Returns:
            ConfigData -- an object with the parsed data
        """
        current_section = ""
        for line in string.split('\n'):
            line = line.strip()
            if self.is_comment(line) or self.is_empty(line):
                continue
            elif self.is_keyval(line):
                keyval = self.parse_key(line)
                self.add_entry(current_section, keyval[0], keyval[1])
            elif self.is_section(line):
                current_section = line[1:-1]
            else:
                raise Exception("Can't process line {}".format(line))
        return self.parseOutput

    def is_keyval(self, line):
        """Checks whether the given line represents a key value pair.

        Arguments:
            line {str} -- the line to be checked

        Returns:
            bool -- true if the line is unindented, in the form key = value \
                    and the key doesn't contain the character ;
        """
        pos = line.find('=')
        return pos != -1 and line[0:pos].find('=') == -1\
            and line[0:pos].find(';') == -1

    def is_section(self, line):
        """Checks whether the given line represents a section.

        Arguments:
            line {str} -- the line to be checked

        Returns:
            bool -- true if the line is unindented, in the form [section]\
                    and section doesn't contain the character ']'
        """
        return len(line) > 2 and line[0] == '[' and line[-1] == ']'\
            and line[1:-1].find(']') == -1

    def is_comment(self, line):
        """Checks whether the given line represents a comment.

        Arguments:
            line {str} -- the line to be checked

        Returns:
            bool -- true if the line is unindented and starts with ; and #
        """

        return len(line) > 0 and (line[0] == ';' or line[0] == '#')

    def is_empty(self, line):
        """Checks whether the given line is empty.

        Arguments:
            line {str} -- the line to be checked

        Returns:
            bool -- true if the line is empty
        """
        return len(line) == 0

    def parse_key(self, line):
        """Parses the line and extracts the key and value from it.

        Arguments:
            line {str} -- the line to be parsed

        Returns:
            list -- in the form [key, value]
        """
        return list(map(lambda l: l.strip(), line.split('=', 1)))

    def add_entry(self, section, key, val):
        """Adds the entry with the given specifications to the ConfiData object.

        section is empty when no section has been entered\
                (i.e. it's a global property)

        Arguments:
            section {str} -- the name of the section
            key     {str} -- the name of the key
            val     {str} -- the value to be stored
        """
        if section == "":  # global property
            self.parseOutput.set_global_property(key, val)
        else:
            self.parseOutput.set_property(section, key, val)


def parse_ini(string):
    """Parses the given string and returns the data in an appropriate form.

    Arguments:
        string {str} -- the string representation of the INI file

    Raises:
        Exception -- if a line is of no known type

    Returns:
        ConfigData -- an object with the parsed data
    """
    return Parser().parse(string)


if __name__ == "__main__":
    sample1 = """
    a = b
    [general]
    appname = configparser
    version = 0.1

    [author]
    name = xmonader
    email = notxmonader@gmail.com

    """
    d = parse_ini(sample1)
    print(d)
