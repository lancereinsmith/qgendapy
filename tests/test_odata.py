from qgendapy.odata import OData, escape_literal, merge_expand


class TestOData:
    def test_select(self):
        params = OData().select("Name", "Email").to_params()
        assert params == {"$select": "Name,Email"}

    def test_filter(self):
        params = OData().filter("IsActive eq true").to_params()
        assert params == {"$filter": "IsActive eq true"}

    def test_orderby(self):
        params = OData().orderby("Name desc").to_params()
        assert params == {"$orderby": "Name desc"}

    def test_expand(self):
        params = OData().expand("Tasks").to_params()
        assert params == {"$expand": "Tasks"}

    def test_chaining(self):
        params = (
            OData()
            .select("Name", "Email")
            .filter("IsActive eq true")
            .orderby("Name asc")
            .expand("Details")
            .to_params()
        )
        assert params == {
            "$select": "Name,Email",
            "$filter": "IsActive eq true",
            "$orderby": "Name asc",
            "$expand": "Details",
        }

    def test_to_params_returns_copy(self):
        odata = OData().select("Name")
        p1 = odata.to_params()
        p2 = odata.to_params()
        assert p1 == p2
        p1["$select"] = "modified"
        assert odata.to_params()["$select"] == "Name"

    def test_empty(self):
        assert OData().to_params() == {}

    def test_overwrite(self):
        params = OData().select("A").select("B").to_params()
        assert params == {"$select": "B"}


class TestODataFromKwargs:
    def test_from_kwargs(self):
        odata = OData.from_kwargs({"$select": "Name", "$filter": "x eq 1", "other": "ignored"})
        params = odata.to_params()
        assert params == {"$select": "Name", "$filter": "x eq 1"}
        assert "other" not in params

    def test_from_kwargs_empty(self):
        odata = OData.from_kwargs({})
        assert odata.to_params() == {}

    def test_from_kwargs_no_dollar_keys(self):
        odata = OData.from_kwargs({"key": "value"})
        assert odata.to_params() == {}


class TestEscapeLiteral:
    def test_no_quotes_unchanged(self):
        assert escape_literal("abc-123") == "abc-123"

    def test_single_quote_doubled(self):
        assert escape_literal("O'Brien") == "O''Brien"

    def test_injection_attempt_neutralized(self):
        # Without escaping, this would close the literal and inject a clause.
        evil = "foo' or '1' eq '1"
        escaped = escape_literal(evil)
        assert escaped == "foo'' or ''1'' eq ''1"
        # When placed inside a filter, the whole thing reads as one literal.
        assert f"StaffKey eq '{escaped}'" == "StaffKey eq 'foo'' or ''1'' eq ''1'"

    def test_empty_string(self):
        assert escape_literal("") == ""


class TestMergeExpand:
    def test_none_expand_returns_odata_unchanged(self):
        odata = OData().select("Name")
        assert merge_expand(None, odata) is odata

    def test_none_expand_and_none_odata(self):
        assert merge_expand(None, None) is None

    def test_string_expand_no_odata(self):
        merged = merge_expand("Tags", None)
        assert merged is not None
        assert merged.to_params() == {"$expand": "Tags"}

    def test_list_expand_joined(self):
        merged = merge_expand(["Tags", "Skillset"], None)
        assert merged is not None
        assert merged.to_params() == {"$expand": "Tags,Skillset"}

    def test_concatenates_with_existing_expand(self):
        odata = OData().expand("Tags").filter("IsActive eq true")
        merged = merge_expand("Skillset", odata)
        assert merged is not None
        params = merged.to_params()
        assert params["$expand"] == "Tags,Skillset"
        assert params["$filter"] == "IsActive eq true"

    def test_does_not_mutate_input_odata(self):
        odata = OData().expand("Tags")
        merge_expand("Skillset", odata)
        assert odata.to_params() == {"$expand": "Tags"}
