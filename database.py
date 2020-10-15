import sqlite3


class DataBaseManger:
    def __init__(self, database_filename):

        self.connection = sqlite3.connect(database_filename)

    def _execute(self, statement, values=None):  # values are optional, some statements have no placeholders to fill in
        #  we create transaction(to avoid database corruption by statements
        #  that are not queries)
        with self.connection:  # this creates a database transaction context
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])  # this happens inside the database transaction and execute the
            # statement  providing any values to the place holders
            return cursor

    def create_table(self, table_name, columns):
        column_with_datatype = [f'{column_name} {data_type}'
                                for column_name, data_type in columns.items()]

        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(column_with_datatype)});
            '''
        )

    def add(self, table_name, data):
        place_holder = ', '.join('?' * len(data))
        column_name = ', '.join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_name})
            VALUES ({place_holder});
            ''',
            column_values,  # passing the optional 'values' argument to _execute
        )

    def delete(self, table_name, criteria):  # criteria ---> a dictionary that maps column_names to the values you
        # want to match
        place_holder = [f'{column_name} = ? ' for column_name in criteria.keys()]
        delete_criteria = ' AND '.join(place_holder)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values()),  # passing the optional 'values' argument to _execute
        )

    def select(self, table_name, criteria=None, order_by=None):

        criteria = criteria or {}  # criteria can be empty by default, because selecting all records in table is
        # alright

        query = f'SELECT * FROM {table_name}'

        if criteria:
            place_holder = [f'{column_name} = ? ' for column_name in criteria.keys()]
            select_criteria = ' AND '.join(place_holder)
            query += f'WHERE {select_criteria}'

        if order_by:
            query += f'ORDER_BY {order_by}'

        self._execute(
            query, tuple(criteria.values()),
        )

    def __del__(self):
        self.connection.close()
