from PyQt5.QtCore import QSettings

def get_postgres_conn_info(selected):
    """ Read PostgreSQL connection details from QSettings stored by QGIS
    """
    settings = QSettings()
    settings.beginGroup(u"/PostgreSQL/connections/" + selected)
    if not settings.contains("database"): # non-existent entry?
        return {}

    conn_info = dict()
    conn_info["host"] = settings.value("host", "", type=str)

    # password and username
    username = ''
    password = ''
    authconf = settings.value('authcfg', '')
    if authconf :
        # password encrypted in AuthManager
        auth_manager = QgsApplication.authManager()
        conf = QgsAuthMethodConfig()
        auth_manager.loadAuthenticationConfig(authconf, conf, True)
        if conf.id():
            username = conf.config('username', '')
            password = conf.config('password', '')
    else:
        # basic (plain-text) settings
        username = settings.value('username', '', type=str)
        password = settings.value('password', '', type=str)

    return username, password

# Test
user, password = get_postgres_conn_info("ULB_PostGIS")
print (user)
print (password)

# Test
user = get_postgres_conn_info("CartULB")
print (user)
print (password)
