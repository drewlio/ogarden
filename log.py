"""
"""
from datetime import datetime, timedelta
from tinydb import TinyDB, Query


class Log:
    """Creates and uses a database for log persistence 
    """

    def __init__(self, file):
        self.db = TinyDB(file)


    def add(self, obj):
        """Add a log entry"""

        # add a timestamp
        obj["isodatetime"] = datetime.isoformat(datetime.now())

        self.db.insert(obj)

        self.clean()


    def clean(self):
        """Keep only 1000 records from the last year. Delete others.
        """

        def older_than_days(d_isoformat, days):
            d = datetime.fromisoformat(d_isoformat)
            age = timedelta(days=days)
            now = datetime.now()
            return d < (now - age)

        self.db.remove(Query().isodatetime.test(older_than_days, 365))

        max_length = 1000
        if len(self.db) > max_length:
            # sort in reverse order (oldest first)
            sorted_records = sorted(self.db.all(), 
                                    key=lambda k: k['isodatetime'],
                                    reverse=True)
            for r in sorted_records[max_length:]:
                self.db.remove(Query().isodatetime == r['isodatetime'])
                print(f"removed {r['isodatetime']}")


    def tail(self, n=1000):
        """Return the last n log entries
        """
        # sort in forward order (newest first)
        sorted_records = sorted(self.db.all(),
                                key=lambda k: k['isodatetime'])
        return sorted_records[-n::]


if __name__ == "__main__":
    from pprint import pprint

    log = Log("log.db")
    #log.add({"testobject": True})
    pprint(log.db.all())

