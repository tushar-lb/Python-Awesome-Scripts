#!/usr/bin/python
#AUTHOR : TUSHAR RAUT

import etcd
import pprint
import json
import commands
import time
 
pp = pprint.PrettyPrinter(indent=4)

class ETCD:
    def create_client(self, host_ip, host_port):
        client = etcd.Client(host=host_ip, port=host_port)
        return client

    def read(self, client, key):
        try:
            print "Inside get for %s" %key
            return client.read(key).value
        except etcd.EtcdKeyNotFound:
            print "error Key Not Found"

    def write(self, client, key, value, dirct=False):
        print "Inside set for key %s and value %s" %(key, value)
        return client.write(key, value, dir=dirct, prevExist=False)

    def multiple_insert(self, client, dir_name):
        #Insertion for Users
        for i in range(10):
            pp.pprint(self.write(client, "%s/u%s" %(dir_name, i), "u%spassword" %i).__dict__)

    def read_recursive(self, client, dir_name):
        return client.read(dir_name, recursive = True)

    def etcd_info(self, client):
        print "Machines"
        pp.pprint(client.machines)
        print "Leader"
        pp.pprint(client.leader)
        print "client stats"
        pp.pprint(client.stats)
        if client.host in client.leader:
            print "client leader stats"
            pp.pprint(client.leader_stats)
        print "client store stats"
        pp.pprint(client.store_stats)

def action(etcd_obj, client, action):
    if action == 1:
        print "Read Opearation"
        key = raw_input("Enter key: ")
        print etcd_obj.read(client, key)
    elif action == 2:
        print "Write operation"
        key = raw_input("Enter key: ")
        value = raw_input("Enter value: ")
        print etcd_obj.write(client, key, value)
    elif action == 3:
        print "Multiple Insert in dir"
        key = raw_input("Enter dir_name ")
        etcd_obj.multiple_insert(client, key)
    elif action == 4:
        print "Read from dir"
        key = raw_input("Enter dir_name ")
        result = etcd_obj.read_recursive(client, key)
        for row in result._children:
            pp.pprint(row)
    elif action == 5:
        print "Bulk Insertion"
        dir_name = raw_input("Enter dir_name ")
        d = raw_input("Enter dict as Value ")
        file_name = "bfile.txt"
        cmd = "echo %s > %s" %(json.dumps(d), file_name)
        print commands.getoutput(cmd)
        url = "curl http://127.0.0.1:2379/v2/keys/%s -XPUT --data-urlencode value@%s"%(dir_name, file_name)
        print commands.getoutput(url)
    elif action == 6:
        etcd_obj.etcd_info(client)
    elif action == 7:
        print "Create Dir"
        key = raw_input("Enter dir path: ")
        value = ""
        print etcd_obj.write(client, key, value, True)
    elif action == 8:
        print "appending data"
        key = raw_input("Enter dir_name: ")
        value = raw_input("Enter value: ")
        print client.write(key, value, append=True)
 
def main():
    host = raw_input("Enter ETCD Host IP: ")
    port = raw_input("Enter ETCD Port: ")
    client = create_client(host, int(port))
    print "Connection object is %s" %client
    etcd_obj = ETCD()
    while True:
        print "========================================================"
        print "1. Get Operation"
        print "2. Set Operation"
        print "3. Multiple Insertions"
        print "4. Read Recursively from Dir"
        print "5. Insert JSON for any key"
        print "6. Leaders, Machines, Leaders Stats, Follower Stats"
        print "7. Create Dir"
        print "8. Append data in Queue in the dir"
        print "9. Exit"
        input_data = raw_input("Enter your action: ")
        if int(input_data) == 9:
            print "Exiting"
            break
        action(etcd_obj, client, int(input_data))
        print "========================================================"
        time.sleep(1)
 
main()
