from PyQt5.QtCore import QSettings

# Function
def GetUserName(PostGIS_Connection_Name):
    qs = QSettings()
    return qs.value("PostgreSQL/connections/%s/username"%PostGIS_Connection_Name)

# Test 
user = GetUserName("ULB_PostGIS")
print (user)

# Test 
user = GetUserName("CartULB")
print (user)
