from dataclasses import dataclass

from qgendapy.models.common import BaseModel, _pascal_to_snake


@dataclass
class Staff(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: str = ""


class TestPascalToSnake:
    def test_simple(self):
        assert _pascal_to_snake("FirstName") == "first_name"

    def test_all_caps_segment(self):
        assert _pascal_to_snake("HTMLParser") == "html_parser"

    def test_single_word(self):
        assert _pascal_to_snake("Name") == "name"

    def test_already_snake(self):
        assert _pascal_to_snake("first_name") == "first_name"

    def test_with_numbers(self):
        assert _pascal_to_snake("Staff2Key") == "staff2_key"


class TestBaseModelFromDict:
    def test_pascal_case_keys(self):
        data = {"FirstName": "Alice", "LastName": "Smith", "Email": "a@b.com"}
        staff = Staff.from_dict(data)
        assert staff.first_name == "Alice"
        assert staff.last_name == "Smith"
        assert staff.email == "a@b.com"

    def test_snake_case_keys(self):
        data = {"first_name": "Bob", "last_name": "Jones", "email": "b@c.com"}
        staff = Staff.from_dict(data)
        assert staff.first_name == "Bob"

    def test_extra_fields_stored(self):
        data = {"FirstName": "Alice", "UnknownField": 42}
        staff = Staff.from_dict(data)
        assert staff.first_name == "Alice"
        assert staff._extra == {"UnknownField": 42}

    def test_missing_fields_use_defaults(self):
        data = {"FirstName": "Alice"}
        staff = Staff.from_dict(data)
        assert staff.first_name == "Alice"
        assert staff.last_name == ""
        assert staff.email == ""

    def test_empty_dict(self):
        staff = Staff.from_dict({})
        assert staff.first_name == ""
        assert staff._extra == {}
