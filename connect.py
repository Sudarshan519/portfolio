import pymysql
import mysql
def mysqlconnect():
    # To connect MySQL database
    conn = mysql.connect(
        host='SudarshanShrestha.mysql.pythonanywhere-services.com',
        user='SudarshanShresth', 
        password = "Asmir123",
        db='SudarshanShresth$default',
        )
      
    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchall()
    print(output)
      
    # To close the connection
    conn.close()
  
# Driver Code
if __name__ == "__main__" :
    mysqlconnect()