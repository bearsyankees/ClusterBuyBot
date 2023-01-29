s = "Rivernorth Managed Duration Municipal Income Fund, Inc. (RMMZ) was bought buy 2 insiders on 2022-02-11 for a price per share of $18.98, filed to the SEC at 2022-02-15 08:17:57. These insiders purchased 6500 shares (a value of $123,353), increasing their total (combined) amount of shares owned by 163%. #stock #stocks"


def get_space(s):
    m = 260
    while s[m] != " ":
        m += 1
    return m
if len(s)>280:
    m = get_space(s)
print("{}...".format(s[:m]))
while len(s)>m:
    s=s[m:].strip()
    print(s)