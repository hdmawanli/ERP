import sqlite3
conn = sqlite3.connect('instance/erp_dev.db')
c = conn.cursor()
cols = [r[1] for r in c.execute("PRAGMA table_info('sales_orders')").fetchall()]
if 'warehouse_id' not in cols:
    c.execute('ALTER TABLE sales_orders ADD COLUMN warehouse_id INTEGER')
    print('Added column warehouse_id')
else:
    print('warehouse_id already exists')
if 'ship_date' not in cols:
    c.execute('ALTER TABLE sales_orders ADD COLUMN ship_date DATE')
    print('Added column ship_date')
else:
    print('ship_date already exists')
conn.commit()
conn.close()
