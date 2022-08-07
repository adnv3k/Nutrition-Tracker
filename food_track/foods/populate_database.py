'''
This file is meant to by run when food data needs to be imported to the database. 
'''

from populate_database.Populator import Populator

p = Populator()
p.migrate_sr_legacy()
p.migrate_branded()
