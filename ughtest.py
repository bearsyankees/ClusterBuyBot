
import re


import pandas as panda
url = 'http://openinsider.com/screener?s=&o=&pl=3&ph=&ll=&lh=&fd=7&fdr=&td=0&tdr=&fdlyl=&fdlyh=6&daysago=&xp=1&vl=25&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=2&nfl=&nfh=&nil=2&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'
tables = panda.read_html(url)
pandaData = tables[11]
data1 = pandaData.to_dict()
data = {re.sub(r'[^\x00-\x7F]',' ', k) : v for k, v in data1.items()}
print(data)

better_data = [{key: data[key][i] for key in data.keys()} for i in range(len(data["X"]))]
print(better_data)
print(better_data[0]["Filing Date"])

"""with requests.Session() as session:
    s = session.get(
        "http://openinsider.com/screener?s=&o=&pl=3&ph=&ll=&lh=&fd=7&fdr=&td=0&tdr=&fdlyl=&fdlyh=6&daysago=&xp=1&vl=25&vh=&ocl=1&och=&sic1=-1&sicl=100&sich=9999&grp=2&nfl=&nfh=&nil=2&nih=&nol=1&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1")
    soup = BeautifulSoup(s.text, 'html.parser')

table = soup.find('table', class_='tinytable')  # locate table
headers = [unicodedata.normalize("NFKD", th.text) for th in
           table.select("tr th")]  # get headers and remove weird whitespace symbol
headers.append("Graph")  # allow spot for graph link

reg_exp = "https:\/\/www\.profitspi\.com\/stock\/stock-charts\.ashx\?chart=.{0,5}&v=stock-chart&vs=.{18}\\\\"

with open("out.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(headers)
    first = [[td.text for td in row.find_all("td")] for row in table.select("tr + tr")]  # get rows of table
    second = [[re.search(reg_exp, a["onmouseover"]).group(0) for a in row.find_all(onmouseover=True)] for row in
              table.select("tr + tr")]  # get graph from table
    for i in range(len(first)):  # merge lists for csv file
        first[i].append(second[i][0])
    wr.writerows(first)  # write to csv file
    f.close()

data = list(csv.DictReader(open("out.csv")))"""