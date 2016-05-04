import os
import sqlite3


class DataSource:
    DATA_SOURCE = None

    def __init__(self, entries=None):
        self.entries = entries
        path = os.path.abspath('model/file_source/data.csv')
        self.file = open(path)

    @staticmethod
    def get_instance():
        if DataSource.DATA_SOURCE is None:
            DataSource.DATA_SOURCE = DataSource()
        return DataSource.DATA_SOURCE

    def read_from_file(self, n):
        self.file.readline()
        self.entries = []
        for i in range(n):
            line = self.file.readline()
            if not line:
                break
            line = line[:-1]
            entry = Entry(line)
            self.entries.append(entry)

        return self.entries

    def set_entries(self, ent):
        self.entries = ent

    def get_entries(self, country=None, operator=None):
        res = []
        for entry in self.entries:
            if country is not None and not entry.Country == country:
                continue
            if operator is not None and not entry.Provider == operator:
                continue
            res.append(entry)

        return res


class Entry:
    def __init__(self, line, x=None, y=None):
        self.line = line
        self.str_num = None
        self.num = None
        self.Country = None
        self.Provider = None
        self.ID = None
        self.Region = None
        self.Ctype = None
        self.IMEI = None
        self.Date = None
        self.Weekday = None
        self.Hour = None
        self.lon = None
        self.lat = None
        if x is None and line is not None:
            self.build()
            self.fix_provider_country()
        else:
            self.lon = x
            self.lat = y

    def build(self):
        inQuotes = self.line.split(',')
        length = len(inQuotes)
        strings = []
        j = 0
        while j < length:
            to_add = inQuotes[j]
            if j != length - 1:
                q = self.get_quotes_num(to_add)
                if to_add[0] == '"' and q % 2 != 0:
                    j, to_add = self.inside_quotes(inQuotes, j, length, to_add)

            if to_add[0] == '"':
                to_add = to_add[1:]
            if to_add[-1] == '"':
                to_add = to_add[:-1]
            if to_add == 'NA':
                to_add = None
            strings.append(to_add)
            j += 1

        self.str_num = strings[0]
        self.num = int(strings[1])
        self.Provider = strings[2]
        self.ID = int(strings[3])
        self.Region = strings[4]
        self.Ctype = strings[5]
        if strings[6]:
            self.IMEI = int(strings[6])

        self.Date = strings[7]
        self.Weekday = strings[8]
        self.Hour = int(strings[9])
        self.lon = float(strings[10])
        self.lat = float(strings[11])

    @staticmethod
    def get_quotes_num(to_add):
        q = 0
        for c in to_add:
            if c == '"':
                q += 1
        return q

    @staticmethod
    def inside_quotes(inQuotes, j, length, toAdd):
        num = 0
        for k in range(j + 1, length):
            s = inQuotes[k]
            j += 1
            if s[0] == '"' and s[-1] == '"':
                toAdd += s
                continue
            if not s[0] == '"':
                toAdd += ',' + s
                if s[-1] == '"':
                    break
        return j, toAdd

    @staticmethod
    def to_json(entry):
        return (
            "{" +
            "\"type\":\"Feature\"," +
            "\"properties\":" +
            "{" +
            "\"scalerank\":18," +
            "\"name\":\"Niagara Falls\"," +
            "\"comment\":null," +
            "\"name_alt\":null," +
            "\"region\":\"North America\"," +
            "\"subregion\":null," +
            "\"featureclass\":\"waterfall\"" +
            "}," +
            "\"geometry\":" +
            "{" +
            "\"type\":\"Point\"," +
            "\"coordinates\":" +
            "[" +
            str(entry.lon) + "," +
            str(entry.lat) +
            "]" +
            "}" +
            "}")

    def fix_provider_country(self):
        prov_and_country = self.Provider
        index = prov_and_country.rfind(",")
        self.Country = prov_and_country[index + 1:].strip(" ")
        self.Provider = prov_and_country[:index].strip(" ")


class SQLDataSource:
    def __init__(self, db_file=None):
        if db_file is None:
            db_file = 'model/database.db'
        self.db_file = db_file

    def get_entries(self, country=None, date_from=None, date_till=None, operator=None):

        if country is None:
            country = "%"

        if operator is None:
            operator = "%"

        query = "SELECT * FROM Entries WHERE country LIKE '{}' AND operator LIKE '{}';".format(country, operator)
        print(query)
        with sqlite3.connect(self.db_file) as conn:
            db_res = conn.execute(query)
            res = []
            for row in db_res:
                new_entry = Entry(None)
                new_entry.Provider = row[1]
                new_entry.Country = row[2]
                new_entry.ID = row[3]
                new_entry.Region = row[4]
                new_entry.Ctype = row[5]
                new_entry.IMEI = row[6]
                new_entry.Date = row[7]
                new_entry.lat = row[8]
                new_entry.lon = row[9]
                res.append(new_entry)
            return res