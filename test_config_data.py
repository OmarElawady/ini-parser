import pytest
import parser
@pytest.fixture
def create_config():
    c = parser.ConfigData()
    # print(c.set_property)
    c.set_property("sec1", "attr1", "val")
    c.set_property("sec1", "attr2", "val2")
    c.set_property("sec2", "attr1", "val3")
    return c


def test_get_property(create_config):
    c = create_config
    assert c.get_property("sec1", "attr1") == "val", "test failed"
    assert c.get_property("sec1", "attr2") == "val2", "test failed"
    assert c.get_property("sec2", "attr1") == "val3", "test failed"


def test_has_property(create_config):
    c = create_config
    assert c.has_property("sec1", "attr1"), "[sec1][attr1] exists"
    assert not c.has_property(
        "sec2", "attr2"), "[sec2][attr2] doesn't exist"


def test_get_section(create_config):
    c = create_config
    assert c.get_section("sec1") == {
        "attr1": "val", "attr2": "val2"}, "Failed to retrieve sec2 section"
    assert c.get_section("sec2") == {
        "attr1": "val3"}, "Failed to retrieve sec2 section"


def test_delete_property(create_config):
    c = create_config
    c.delete_property("sec1", "attr2")
    assert not c.has_property("sec1", "attr2"), "Property is not removed"
    assert c.has_property("sec1", "attr1"), "attr1 should not be touched"


def test_sget_global_property(create_config):
    c = create_config
    c.set_global_property("a", "c")
    assert c.get_global_property(
        "a") == "c", "Didn't add the global attribute 'a'"


def test_len(create_config):
    c = create_config
    assert len(c) == 2, "sections count is 2 not {}".format(
            len(c))


def test_has_section(create_config):
    c = create_config
    assert c.has_section("sec1"), "sec1 exists!"
    assert c.has_section("sec2"), "sec2 exists!"
    assert not c.has_section("sec3"), "sec3 doesn't exist!"
