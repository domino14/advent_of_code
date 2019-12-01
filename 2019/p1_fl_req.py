def fl_req(mass):
    d, m = divmod(mass, 3)
    fuel_req = d - 2
    addlf = 0
    f = fuel_req

    while f > 0:
        dd, _ = divmod(f, 3)
        f = dd - 2
        if f <= 0:
            break

        addlf += f
    
    return fuel_req + addlf
