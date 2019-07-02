import pytest
import parser
@pytest.fixture
def create_config():
    c = parser.ConfigData()
    #print(c.setProperty)
    c.setProperty("sec1", "attr1", "val")
    c.setProperty("sec1", "attr2", "val2")
    c.setProperty("sec2", "attr1", "val3")
    return c

def test_getProperty(create_config):
    c = create_config
    assert c.getProperty("sec1", "attr1") == "val", "test failed"
    assert c.getProperty("sec1", "attr2") == "val2", "test failed"
    assert c.getProperty("sec2", "attr1") == "val3", "test failed"
def test_hasProperty(create_config):
    c = create_config
    assert c.hasProperty("sec1", "attr1") == True , "[sec1][attr1] exists"
    assert c.hasProperty("sec2", "attr2") == False, "[sec2][attr2] doesn't exist"
def test_get_section(create_config):
    c = create_config
    assert c.getSection("sec1") == {"attr1" : "val", "attr2": "val2"}, "Failed to retrieve sec2 section"
    assert c.getSection("sec2") == {"attr1" : "val3"}, "Failed to retrieve sec2 section"
def test_deleteProperty(create_config):
    c = create_config
    c.deleteProperty("sec1", "attr2")
    assert c.hasProperty("sec1", "attr2") == False, "Property is not removed"
    assert c.hasProperty("sec1", "attr1") == True, "attr1 should not be touched"
def test_sget_global_property(create_config):
    c = create_config
    c.setGlobalProperty("a", "c")
    assert c.getGlobalProperty("a") == "c", "Didn't add the global attribute 'a'"
def test_sections_count(create_config):
    c = create_config
    assert c.sectionsCount() == 2, "sections count is 2 not {}".format(c.sectionsCount())
def test_has_section(create_config):
    c = create_config
    assert c.hasSection("sec1") == True, "sec1 exists!"
    assert c.hasSection("sec2") == True, "sec2 exists!"
    assert c.hasSection("sec3") == False, "sec3 doesn't exist!"
