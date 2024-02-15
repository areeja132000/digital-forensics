import sqlite3
import sys
import datetime

filename = ''
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Error! - No History File Specified!")
    exit()

try:
    file = open(filename)
    file.close()
except:
    print("Error! - File Not Found!")
    exit()

print("Source File: {}".format(filename))
sqliteConnection = sqlite3.connect(filename)
cursor = sqliteConnection.cursor()

sqlite_select_Query = "SELECT COUNT(*) FROM downloads"
cursor.execute(sqlite_select_Query)
record = cursor.fetchall()
print("Total Downloads: {}".format(record[0][0]))

#print("LONGEST DOWNLOAD")
max_time=0
result=0
sqlite_select_Query = "SELECT * FROM downloads"
cursor.execute(sqlite_select_Query)
record = cursor.fetchall()
for row in record:
    start_time = row[4]
    end_time = row[11]
    total_time = end_time-start_time
    #print("{}: start- {} end- {} total- {}".format(row[0], start_time, end_time, total_time))
    if total_time > max_time:
        max_time=total_time
        result = row[0]

sqlite_select_Query = "SELECT * FROM downloads WHERE id={}".format(result)
cursor.execute(sqlite_select_Query)
record = cursor.fetchall()
print("File Name: {}".format(record[0][2].split("\\")[-1]))
print("File Size: {}".format(record[0][6]))

sqlite_select_Query = "SELECT COUNT(DISTINCT term) FROM keyword_search_terms"
cursor.execute(sqlite_select_Query)
record = cursor.fetchall()
print("Unique Search Terms: {}".format(record[0][0]))

sqlite_select_Query = """SELECT keyword_search_terms.url_id, keyword_search_terms.term, urls.id, urls.last_visit_time
FROM keyword_search_terms
INNER JOIN urls ON keyword_search_terms.url_id=urls.id
ORDER BY urls.last_visit_time DESC"""
cursor.execute(sqlite_select_Query)
record = cursor.fetchall()
print("Most Recent Search: {}".format(record[0][1]))
date = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=record[0][3])
print("Most Recent Search Date/Time: {}".format(date.strftime('%Y-%b-%d %H:%M:%S')))
cursor.close()

