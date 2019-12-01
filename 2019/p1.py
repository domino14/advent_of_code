import requests

from get_data import get_data_lines
from p1_fl_req import fl_req

inp  = get_data_lines(1)
print(inp)

req = 0
for l in inp:
    x = int(l)
    d, m = divmod(x, 3)

    req += (d - 2)

print(req)

# part 2
req = 0
for l in inp:
    x = int(l)
    req += fl_req(x)
# not 5073331
print(req)