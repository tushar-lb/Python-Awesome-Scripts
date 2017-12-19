class Storage(object):
    '''
    Base Parent Class
    '''
    def get_info(self):
        print('Storage info..')

    def update_info(self):
        print('Update storage info..')


class Redis(Storage):
    '''
    Derived from Storage
    '''
    def redis_conn(self):
        print('Connection Done!')


class SQlite(Storage):
    '''
    Derived from SQLite
    '''
    def sqlite_query(self):
        print('Executing query!')


def main():
    '''
    Main function
    :return:
    '''
    storage = Storage()
    storage.get_info()

    # Redis also includes all functions from parent class (Storage)
    red = Redis()
    red.get_info()
    red.redis_conn()

    # SQlite is called (the child class), inherits from Storage (parent class)
    sql = SQlite()
    sql.update_info()
    sql.sqlite_query()


if __name__ == '__main__':
    main()

