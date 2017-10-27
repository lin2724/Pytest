import sqlite3


class DBItem:
    def __init__(self, name, type_str, is_primary=False):
        self.name = name[:]
        self.value = None
        self.type_str = type_str[:]
        self.is_primary = is_primary

        pass


class DBRow:
    def __init__(self):
        self.item_list = list()
        self.do_init()
        pass

    def __str__(self):
        ret_str = ''
        for item in self.item_list:
            ret_str += item.name + ' : ' + str(item.value) + '\n'
        return ret_str

    def do_init(self):

        pass

    def load(self, tuple_row):
        for idx, item in enumerate(self.item_list):
            item.value = tuple_row[idx]
        pass

    def generate_select_str(self, table_name):
        ret_str = ''
        for idx, item in enumerate(self.item_list):
            ret_str += table_name + '.' + item.name
            if idx != len(self.item_list):
                ret_str += ','
        pass


class DBRowHuaBan(DBRow):
    def do_init(self):
        self.item_list.append(DBItem('board_id', 'INT'))
        self.item_list.append(DBItem('url', 'CHAR'))
        self.item_list.append(DBItem('pin_id', 'INT'))
        self.item_list.append(DBItem('is_done', 'INT'))
        pass


class DBHandler:
    def __init__(self):
        self.con = None
        pass

    def load(self, db_file_path):
        self.con = sqlite3.connect(db_file_path)
        pass

    def do_init(self):
        pass

    def add_table(self, table_name, db_row):
        create_command = self.generate_create_table_str(table_name, db_row)
        print create_command
        self.con.execute(create_command)
        self.con.commit()
        pass

    def generate_create_table_str(self, table_name, db_row):
        ret_str = ''
        ret_str += 'CREATE TABLE IF NOT EXISTS %s(' % table_name
        for idx, item in enumerate(db_row.item_list):
            ret_str += item.name + ' ' + item.type_str + ' '
            if item.is_primary:
                ret_str += 'PRIMARY KEY'
            if idx != len(db_row.item_list) - 1:
                ret_str += ','
        ret_str += ')'
        return ret_str
        pass

    def get_row(self, table_name, db_row, limit):
        command_str = ''

    def exist(self):
        if self.con:
            self.con.close()


def test():
    print type(str)
    handler = DBHandler()
    handler.load('test.db')
    handler.add_table('huaban', DBRowHuaBan())
    pass

if __name__ == '__main__':
    test()