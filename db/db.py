import sqlite3

con = sqlite3.connect('C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\db\\user.db')

cursor = con.execute("SELECT ID,BG,HIGHLIGHT,XP from PROFILE_DATA_BASIC where ID=435812068290199553")

print(cursor)
row = 0
for row in cursor:
    continue

print(row)

try:
    if 435812068290199553 == row[0]:
        print("ID= ",row[0])
        print("BG= ",row[1])
        print("HIGHLIGHT= ",row[2])
        print("XP= ",row[3])
        
except:
    print("not found")


con.close()