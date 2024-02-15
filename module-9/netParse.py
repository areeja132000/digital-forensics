import csv
import sys
import datetime
import operator

def my_key(item):
    temp = item.split(".")
    return int(temp[-1])

filename = ''
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Error! - No Log File Specified!")
    exit()

try:
    log_file = open(filename)
except:
    print("Error! - File Not Found!")
    exit()

reader = csv.reader(log_file)
infected_systems = []
c2_servers = []
earliest_date = 0
c2_to_data = {}
for row in reader:
    #print(row)
    connection_established = row[0]
    #print(connection_established)
    source_ip = row[1]
    #print(source_ip)
    dest_ip = row[2]
    #print(dest_ip)
    source_port = row[3]
    #print(source_port)
    dest_port = row[4]
    #print(dest_port)
    bytes_sent_source_to_dest = row[5]
    bytes_received_dest_to_source = row[6]
    total_bytes_transferred = row[7]
    c2_ports = ["1337", "1338", "1339", "1340"]
    if source_ip[0:9] == '10.10.10.' and dest_port in c2_ports:
        if earliest_date == 0:
            earliest_date = int(connection_established)
        else:
            if (int(connection_established) < earliest_date):
                earliest_date = int(connection_established)
        if source_ip not in infected_systems:
            infected_systems.append(source_ip)
        if dest_ip not in c2_servers:
            c2_servers.append(dest_ip)
        if dest_ip in c2_to_data:
            c2_to_data[dest_ip] += int(bytes_sent_source_to_dest)
        else:
            c2_to_data[dest_ip] = int(bytes_sent_source_to_dest)
log_file.close()

print("Source File: {}".format(filename))

print("Systems Infected: {}".format(len(infected_systems)))
sorted_infected_systems = sorted(infected_systems, key=my_key)
print("Infected System IPs:\n{}".format(sorted_infected_systems))

print("C2 Servers: {}".format(len(c2_servers)))
c2_servers.sort()
print("C2 Server IPs:\n{}".format(c2_servers))

print("First C2 Connection: {} UTC".format(datetime.datetime.fromtimestamp(int(earliest_date)).strftime('%Y-%b-%d %H:%M:%S')))
sorted_data = sorted(c2_to_data.items(), key=operator.itemgetter(1), reverse=True)
print("C2 Data Totals: {}".format(sorted_data))