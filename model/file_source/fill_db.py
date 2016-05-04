from model.file_source.data_source import DataSource

import sqlite3

create_str = "CREATE TABLE Entries (" \
             "id INTEGER PRIMARY KEY AUTOINCREMENT," \
             "operator VARCHAR(100)," \
             "country VARCHAR(100)," \
             "entry_id VARCHAR(15)," \
             "region VARCHAR(100)," \
             "c_type VARCHAR(15)," \
             "imei VARCHAR(15)," \
             "action_date DATETIME," \
             "latitude DECIMAL(2, 20)," \
             "longitude DECIMAL(2, 20));" \
             "CREATE INDEX country_index ON Entries (country);" \
             "CREATE INDEX operator_index ON Entries (operator);" \
             "CREATE INDEX date_index ON Entries (action_date); "

insert_str = "INSERT INTO Entries " \
             "(operator, country, entry_id, region, " \
             "c_type, imei, action_date, latitude, longitude) " \
             "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"

with sqlite3.connect('database.db') as conn:
    data_source = DataSource.get_instance()
    entries = data_source.read_from_file(200000)
    for entry in entries:
        statement = insert_str.format(entry.Provider, entry.Country, entry.ID, entry.Region,
                                      entry.Ctype, entry.IMEI, entry.Date, entry.lat, entry.lon)
        conn.execute(statement)
    conn.commit()

