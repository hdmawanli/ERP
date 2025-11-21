import sqlite3
fn='instance/erp_dev.db'
try:
    conn=sqlite3.connect(fn)
except Exception as e:
    print('open error',e)
    raise
c=conn.cursor()
print('tables in',fn)
for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    print('-',r[0])
print('\nPRAGMA table_info(sales_orders):')
for r in c.execute("PRAGMA table_info('sales_orders')").fetchall():
    print(r)
conn.close()
