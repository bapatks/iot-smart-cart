##import firebase_admin
##from firebase_admin import credentials

##cred = credentials.Cert('path/to/serviceKey.json')
##firebase_admin.initialize_app(cred, {
##    'databaseURL' : 'https://my-db.firebaseio.com'
##})

def table_get_wt(barcode):
    table = {"321456": ["Brown Rice", 2.0, 5], "926571": ["Sugar", 1.0, 6]}
    if barcode in table:
        return table[barcode][1]
    else:
        return 0
