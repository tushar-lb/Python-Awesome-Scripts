from random import randrange


class Storage(object):
    name = None
    type = None

    @staticmethod
    def get_storage(x):
        if x == 0:
            return Redis()
        if x == 1:
            return SQLite()


class Redis(Storage):
    name = 'Redis'
    type = 'key-value'


class SQLite(Storage):
    name = 'SQlite'
    type = 'RDBMS'


def main():
    '''
    Main function
    :return:
    '''
    # Create 5 random Storage
    for _ in range(5):
        s = Storage.get_storage(randrange(5))
        print(s.name, s.type)


if __name__ == '__main__':
    main()
