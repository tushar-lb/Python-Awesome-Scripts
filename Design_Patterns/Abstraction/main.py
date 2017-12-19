import os


class Storage(object):

    @staticmethod
    def update_storage_info():
        host_ip = os.environ('HOST_IP')
        host_port = os.environ('HOST_PORT')
        print("Updated info, %s:%s" % (host_ip, host_port))


def main():
    '''
    Main funcion
    :return:
    '''
    # User does not need to pass storage host details
    Storage.update_storage_info()


if __name__ == '__main__':
    main()

