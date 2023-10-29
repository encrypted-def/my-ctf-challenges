from flask import Flask, request, render_template
import random

FLAG = "WACON{e0d1708636f669cd7596d6d81efcb1e117f}"

random.seed(13)

app = Flask(__name__)

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

challenges = [f'Chal-{i:02d}' for i in range(50)]

def solve_list_init():
    prob_for_challs = [random.randint(1,100) for _ in range(len(challenges))]
    team_solved = {}
    team_num = len(teams)
    chal_num = len(challenges)
    for i in range(team_num):
        L = []
        for j in range(len(challenges)):
            if random.randint(1,101) < prob_for_challs[j]:
                L.append(challenges[j])
        team_solved[teams[i]] = L
    return team_solved

def get_ranking(scores):
    L = []
    solver_num = {}
    for team in teams:
        for chal in team_solved[team]:
            if chal not in solver_num:
                solver_num[chal] = 0
            solver_num[chal] += 1
    
    for team in teams:
        tot = 0
        for chal in team_solved[team]:
            tot += scores[solver_num[chal] - 1]
        L.append([tot, team])
    L.sort(key=lambda x : (-x[0], x[1]))
    return L
    
@app.route('/')
def index():
    return render_template('index.html', teams=teams)

@app.route('/team/<team_name>')
def team(team_name):
    global team_solved
    if team_name in teams:
        team_problems = team_solved[team_name]

    return render_template('team.html', team_name=team_name, team_problems=team_problems)

@app.route('/scoreboard_requested')
def scoreboard_requested():
    return render_template('scoreboard_requested.html', ranking_list=expected_ranking_list)

@app.route('/setting')
def setting():
    L = [(str(i), 1010-10*i) for i in range(1,len(teams)+1)]
    return render_template('setting.html', L=L)

@app.route('/check', methods=['POST'])
def check():
    msg = ''
    try:
        score_from_input = [int(request.form[f'input{i}']) for i in range(1,len(teams)+1)]
        for i in range(len(teams)-1):
            if score_from_input[i] <= score_from_input[i+1]:
                msg = f"[-] {i+1}-solve score({score_from_input[i]}) is less than or equal to {i+1}-solve score({score_from_input[i+2]})\n"

            if score_from_input[0] > 10**9 or score_from_input[len(teams)-1] < 1:
                msg += f"[-] Some score is out range of 1 to 1,000,000,000."
    
    except:
        msg = '[-] Invalid data.'
    
    if msg: # some error has been occured
        ranking = []
    else:
        ranking = get_ranking(score_from_input)
        if all(ranking[i][1] == expected_ranking_list[i][1] for i in range(len(teams))):
            msg = FLAG
        else:
            msg = "I don't expect this..."
    
    return render_template('check.html', ranking=ranking, msg=msg)

team_solved = solve_list_init()
scores_ans = random.sample(range(100,100000),len(teams))
scores_ans.sort(reverse=True)
expected_ranking_list = get_ranking(scores_ans)
if __name__ == '__main__':
    app.run()