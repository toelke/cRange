
def range_left(l, r):
	return (l[0] << r[0], l[1] << r[1], 0)

def range_right(l, r):
	return (l[0] >> r[0], l[1] >> r[1], 0)

def range_minus(l, r):
	ma = l[0] - r[1]
	mi = l[1] - r[0]
	
	if ma < mi:
		(ma, mi) = (mi, ma)

	return (mi, ma, 0)

def range_plus(l, r):
	ma = l[0] + r[0]
	mi = l[1] + r[1]
	
	if ma < mi:
		(ma, mi) = (mi, ma)

	return (mi, ma, 0)

def range_mul(l, r):
	table = [x*y for x in l[:2] for y in r[:2]]

	ma = max(table)
	mi = min(table)
	
	return (mi, ma, 0)

def range_div(l, r):
	table = [x/y for x in l[:2] for y in r[:2] if y != 0]
	print l, r, table

	if len(table) < 1:
		return (0, 0, 0)
	ma = max(table)
	mi = min(table)
	
	return (mi, ma, 0)
