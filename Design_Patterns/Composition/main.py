class Redis(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


class MySQL(object):

    def __init__(self, connection):
        self.connection = connection


class DB(object):

    def __init__(self, ip, port, connections):
        self.redis = Redis(ip, port)
        self.mysql = MySQL(connections)

    def display_ip_port(self):
        print(self.redis.ip)
        print(self.redis.port)


def main():
    '''
    Main function
    :return:
    '''
    db = DB('127.0.0.1', '2379', 100)
    db.display_ip_port()


if __name__ == '__main__':
    main()

