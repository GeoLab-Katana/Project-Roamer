import math
import random
import sqlite3

from file_source.data_source import DataSource, Entry
from reducer.translator import Translator

GEO_LU_Y = 43.778536
GEP_LU_X = 40.173705
GEO_RU_Y = 43.154278
GEO_RU_X = 46.757617
GEO_RD_Y = 41.001847
GEO_RD_X = 46.603808
GEO_LD_Y = 41.126098
GEO_LD_X = 40.088915
GRID_SIZE_X = 10000
GRID_SIZE_Y = 5000


def add_to_regional_db(_list):
    insert_str = "INSERT INTO RegionalEntries " \
                 "(operator, country, entry_id, region, " \
                 "c_type, imei, action_date, latitude, longitude) " \
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"

    with sqlite3.connect('database.db') as conn:
        for entry in _list:
            statement = insert_str.format(entry.Provider, entry.Country, entry.ID, entry.Region,
                                          entry.Ctype, entry.IMEI, entry.Date, entry.lat, entry.lon)
            conn.execute(statement)
        conn.commit()


class Reducer:
    def __init__(self, filename):
        self._filename = filename

    def reduce_data(self):
        data_source = DataSource.get_instance()
        handler = data_source.read_from_file(1000000)
        start_c = (GEO_LD_X, GEO_LD_Y)
        end_c = (GEO_RU_X, GEO_RU_Y)
        self.reduce_entries(start_c, end_c, handler, data_source)

    def reduce_entries(self, start_c, end_c, entries, dt_src):
        grid = {}
        countries = {}
        region = {}
        region_countries = {}
        size = (GRID_SIZE_X, GRID_SIZE_Y)
        translator = Translator(start_c, end_c, size)
        for entry in entries:
            x = entry.lon
            y = entry.lat
            x, y = translator.translate_to_grid((x, y))
            count = get_from_grid(grid, x, y)
            set_to_grid(grid, x, y, count + 1)
            arg = (entry.Region, entry.Country)
            if (x, y) not in countries:
                countries[(x, y)] = []
            countries[(x, y)].append(arg)
            if arg[0] not in region:
                region[arg[0]] = {}
            if arg[0] not in region_countries:
                region_countries[arg[0]] = {}
            reg_c = region_countries[arg[0]]
            if (x, y) not in reg_c:
                reg_c[(x, y)] = []
            reg_c[(x, y)].append(arg)
            region_countries[arg[0]] = reg_c

            count = get_from_grid(region[arg[0]], x, y)
            _reg_dict = region[arg[0]]
            set_to_grid(_reg_dict, x, y, count + 1)
            region[arg[0]] = _reg_dict

        coordinate_list = self.reduce_map(grid, size, translator, countries)
        dt_src.set_entries(coordinate_list)
        # for key, value in region.items():
        #     print(key)
            # _list = self.reduce_map(value, size, translator, region_countries[key])
            # add_to_regional_db(_list)
            # print(len(_list))

    def reduce_map(self, grid, size, translator, countries):
        grid = self._avg_for_each(grid, countries)
        average = self._get_grid_avg(grid)
        min_val = self._remove_trashold(grid, average)
        grid = self._scale(grid, min_val)
        coordinate_list = self._generate_list(grid, translator, countries)
        return coordinate_list
        # print(coordinate_list)
        # print(len(coordinate_list))

    def _avg_for_each(self, grid, countries):
        new_grid = {}
        for key, val in grid.items():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # old_val = get_from_grid(grid, i, j)
                    x = key[0] + i
                    y = key[1] + j
                    average = get_average(grid, (x, y))
                    if average > 0:
                        new_grid[(x, y)] = average
                        if (x, y) not in countries:
                            countries[(x, y)] = []
                        _ls = countries[(key[0], key[1])]
                        for _ in range(0, average):
                            countries[(x, y)].append(random.choice(_ls))
        return new_grid

    def _get_grid_avg(self, grid):
        average = 0
        for _, val in grid.items():
            average = max(average, val) # (average + val) / 2
        return int(math.sqrt(int(math.sqrt(average))))

    def _remove_trashold(self, grid, average):
        _min = 100000000000
        for key, val in grid.items():
            if val < average:
                grid[key] = 0
            else:
                _min = min(grid[key], _min)
        return _min

    def _scale(self, grid, min_val):
        _ls = []
        for key, val in grid.items():
            old_val = get_from_grid(grid, key[0], key[1])
            if old_val > min_val:
                diff = int(old_val / min_val)
                # new_val = old_val - min_val * diff + 1
                new_val = diff
                set_to_grid(grid, key[0], key[1], new_val)
            else:
                _ls.append(to_str(key[0], key[1]))
        for key in _ls:
            del grid[key]
        return grid

    def _generate_list(self, grid, translator, countries):
        _list = []
        for key, val in grid.items():
            if val > 0:
                for _ in range(0, val):
                    x, y = translator.random_in_coordinate(key)
                    _ls = countries[(key[0], key[1])]
                    region, country = random.choice(_ls)
                    entry = Entry(None, x=x, y=y)
                    entry.Country = country
                    entry.Region = region
                    _list.append(entry)
        return _list


def get_average(grid, coord):
    x, y = coord
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            sum += get_from_grid(grid, x + i, y + j)
    return int(sum / 9)


def set_to_grid(grid, x, y, val):
    key = to_str(x, y)
    grid[key] = val


def to_str(x, y):
    return x, y


def get_from_grid(grid, x, y):
    if to_str(x, y) in grid:
        return grid[to_str(x, y)]
    return 0