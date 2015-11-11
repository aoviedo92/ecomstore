product_per_pag = [1, 2, 3, 4, 5, 6, 7, 8]
prod_x_row = 3
product_row = []  # lista que almacena filas de prod de 3 en e [[p1,p2,p3],[p4,p5,p6]...]
row = []
rest = []
while len(product_per_pag):
    product = product_per_pag.pop()
    row.append(product)
    rest.append(product)
    if len(row) == prod_x_row:
        product_row.append(row)
        row = []
        rest = []
product_row.append(rest)
print(product_row)