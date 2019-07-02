class ConfigData:

    def __init__(self):
        self.data = {}
    def setProperty(self, section, key, val):
        section = section.lower()
        key = key.lower()
        val = val.lower()
        if not section in self.data:
            self.data[section] = {}
        self.data[section][key] = val
    def hasSection(self, section):
        section = section.lower()
        return section in self.data
    def getProperty(self, section, key):
        section = section.lower()
        key = key.lower()
        return self.data[section][key]
    def sectionsCount(self):
        return len(list(filter(lambda x: type(x) == dict, self.data.values())))
    
    def hasProperty(self, section, key):
        section = section.lower()
        key = key.lower()
        return section in self.data and key in self.data[section]
    def getSection(self, section):
        section = section.lower()
        return self.data[section]
    def deleteProperty(self, section, key):
        section = section.lower()
        key = key.lower()
        del self.data[section][key]
    def getGlobalProperty(self, key):
        key = key.lower()
        return self.data[key]
    def setGlobalProperty(self, key, val):
        key = key.lower()
        val = val.lower()
        self.data[key] = val
    def toIniString(self):
        return str(self.data)
class Parser:
    def __init__(self):
        self.parseOutput = ConfigData()

    def parse(self, string):
        currentSection = ""
        for line in string.split('\n'):
            line = line.strip()
            if self.is_comment(line) or self.is_empty(line):
                continue
            elif self.is_keyval(line):
                keyval = self.parseKey(line)
                self.addEntry(currentSection, keyval[0], keyval[1])
            elif self.is_section(line):
                currentSection = line[1:-1]
            else:
                raise Exception("Can't process line {}".format(line))
        return self.parseOutput
    def is_keyval(self, line):
        pos = line.find('=');
        return pos != -1 and line[0:pos].find('=') == -1 and line[0:pos].find(';') == -1
    def is_section(self, line):
        return len(line) > 2 and line[0] == '[' and line[-1] == ']' and line[1:-1].find(']') == -1
    def is_comment(self, line):
        return len(line) > 0 and (line[0] == ';' or line[0] == '#')
    def is_empty(self, line):
        return len(line) == 0
    def parseKey(self, line):
        return list(map(lambda l : l.strip(), line.split('=', 1)))
    def addEntry(self, section, key, val):
        if section == "": # global property
            self.parseOutput.setGlobalProperty(key, val)
        else:
            self.parseOutput.setProperty(section, key, val)

            


sample1 = """
a = b
[general]
appname = configparser
version = 0.1

[author]
name = xmonader
email = notxmonader@gmail.com

"""
def parseIni(string):
    return Parser().parse(string)
if __name__ == "__main__":    
    d = parseIni(sample1)
    # doAssert(d.sectionsCount() == 2)
    assert (d.getProperty("general", "appname") == "configparser")
    assert (d.getProperty("general","version") == "0.1")
    assert (d.getProperty("author","name") == "xmonader")
    assert (d.getProperty("author","email") == "notxmonader@gmail.com")

    d.setProperty("author", "email", "alsonotxmonader@gmail.com")
    assert (d.getProperty("author","email") == "alsonotxmonader@gmail.com")
    assert (d.hasSection("general") == True)
    assert (d.hasSection("author") == True)
    assert (d.hasProperty("author", "name") == True)
    d.deleteProperty("author", "name")
    assert (d.hasProperty("author", "name") == False)
    assert (d.getGlobalProperty("a") == "b")
    assert (d.sectionsCount() == 2)
    print(d.toIniString())

