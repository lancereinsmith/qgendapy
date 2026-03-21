from qgendapy.resources.schedule import _date_chunks


class TestDateChunks:
    def test_within_limit(self):
        chunks = _date_chunks("2024-01-01", "2024-03-01")
        assert chunks == [("2024-01-01", "2024-03-01")]

    def test_exactly_100_days(self):
        chunks = _date_chunks("2024-01-01", "2024-04-10")
        assert chunks == [("2024-01-01", "2024-04-10")]

    def test_over_100_days_splits(self):
        chunks = _date_chunks("2024-01-01", "2024-04-11")
        assert len(chunks) == 2
        assert chunks[0] == ("2024-01-01", "2024-04-10")
        assert chunks[1] == ("2024-04-11", "2024-04-11")

    def test_large_range(self):
        chunks = _date_chunks("2024-01-01", "2024-12-31")
        # 366 days -> 4 chunks
        assert len(chunks) == 4
        # Verify no gaps
        for i in range(len(chunks) - 1):
            end = chunks[i][1]
            next_start = chunks[i + 1][0]
            from datetime import date, timedelta

            e = date.fromisoformat(end)
            ns = date.fromisoformat(next_start)
            assert ns - e == timedelta(days=1)
        # Verify full coverage
        assert chunks[0][0] == "2024-01-01"
        assert chunks[-1][1] == "2024-12-31"

    def test_single_day(self):
        chunks = _date_chunks("2024-01-01", "2024-01-01")
        assert chunks == [("2024-01-01", "2024-01-01")]
