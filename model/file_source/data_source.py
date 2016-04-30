class DataSource:
    def __init__(self, entries=None):
        self.entries = entries

    @staticmethod
    def read_from_file(data_file, n):
        data_file.readline()
        entries = []
        for i in range(n):
            line = data_file.readline()
            if not line:
                break
            line = line[:-1]
            entry = Entry(line)
            entries.append(entry)

        return entries

    def set_entries(self, entries):
        self.entries = entries

    def get_entries(self):
        return self.entries


class Entry:
    def __init__(self, line):
        self.line = line
        self.str_num = None
        self.num = None
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
        self.build()

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