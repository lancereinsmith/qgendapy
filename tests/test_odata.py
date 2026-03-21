from qgendapy.odata import OData


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
