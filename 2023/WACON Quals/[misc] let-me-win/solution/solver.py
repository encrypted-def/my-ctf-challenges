from bs4 import BeautifulSoup
import requests
from z3 import *

BASE_URL = 'http://175.118.127.123:5000'

teams = '''zer0cats
CheckTheSign
C4T BuT M3W
idk
kalmaronion
HikeBoy
justCatchTheFish
r3kabunny
SNSD
organi-cats
thequackerscrew
1daysober
More Fried Elite Duck
Black Butterflies
Project Sakura
QQQ
ShyKOR
Goose N
MINUS
Balsamic Vinegar
Never Stop Exploding
DiceDang
The Round Network Society
796e74
The Moose
Upper Guesser
HackingForBeer
Waffle Bacon
ChordBlue
mhackaroni
Watermelon Paddler
Perfect Pink
Katzekatbin
The Quack
Shellfish
Dragon Sushi
Emu Eggs Benny
YGY
OsakaWesterns
Polygroot
Dragon Vector
LCDC
127
Eat, Sleep, Misc, Repeat
Nu0L
o0ps
Bubble Tea Deliverers
Dashwhackers
A*C*E
CloseToAll
Deficit
squareimentary
daejeonelectricdecomposer
none2root
Inverselab
Ever Stop Exploiting
copyn
SunBugs
FBISEC
defined
NEWSEC'''.split('\n')

def parse_challenges(teamname):
    url = BASE_URL + '/team/' + teamname
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    li_tags = soup.find_all('li')
    challs = []
    for li in li_tags:
        if li.text:
            challs.append(li.text)
    return challs


def get_rank_list():
    url = BASE_URL + '/scoreboard_requested'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    li_tags = soup.find_all('li')
    ranks = []
    for li in li_tags:
        if li.text:
            ranks.append(li.text)
    return ranks


def find_solution():
    vars = [Int(f'var{i}') for i in range(len(teams))]
    eqs = []
    for team in ranks:
        eq = 0
        for chal in team_solved[team]:
            eq += vars[occur[chal]-1]
        eqs.append(eq)
    
    z = Solver()
    z.add(vars[-1] > 0)
    z.add(vars[0] < 10**9)
    for i in range(len(teams)-1):
        z.add(eqs[i] > eqs[i+1])
        z.add(vars[i] > vars[i+1])
    
    if z.check() == sat:
        model = z.model()
        ret = []
        for var in vars:
            ret.append(model[var].as_long())
        print(ret)
    
    else:
        print("unsat")
        exit(-1)

    return ret

def send_query(sol):
    url = BASE_URL + '/check'
    data = {}
    for i in range(len(teams)):
        data[f"input{i+1}"] = str(sol[i])
    
    resp = requests.post(url, data=data)
    t = resp.text
    if "WACON" not in t:
        print("nono..")
    else:
        i1 = t.find("WACON")
        i2 = t.find("}")
        print(t[i1:i2+1])

team_solved = {}
occur = {}

for team in teams:
    team_solved[team] = parse_challenges(team)
    for chal in team_solved[team]:
        if chal not in occur:
            occur[chal] = 0
        occur[chal] += 1

ranks = get_rank_list()
#print(ranks)
#exit()

print("Parse done")

print("z3 gogo")
sol = find_solution()
send_query(sol)
