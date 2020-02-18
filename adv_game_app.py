from flask import Flask,render_template,request
import random

map_dict={
	0:{'Name':'Forest-1','openPaths':(6,7,8,2)},
	1:{'Name':'Forest-2','openPaths':(3,6,7,11)},
	2:{'Name':'Forest-3','openPaths':(0,10,11,12)},
	3:{'Name':'Forest-4','openPaths':(1,)},
	4:{'Name':'Canyon Bottom','openPaths':(13,)},
	5:{'Name':'Stone Barrow','openPaths':(8,)},
	6:{'Name':'Clearing-1','openPaths':(0,1,7)},
	7:{'Name':'Forest Path','openPaths':(0,1,9)},
	8:{'Name':'West of House','openPaths':(5,9,10)},
	9:{'Name':'North of House','openPaths':(7,8,14)},
	10:{'Name':'South of House','openPaths':(2,8,14)},
	11:{'Name':'Clearing-2','openPaths':(2,12,14)},
	12:{'Name':'Canyon View','openPaths':(2,11,13)},
	13:{'Name':'Rocky Ledge','openPaths':(4,12)},
	14:{'Name':'Behind the House','openPaths':(11,15)},
	15:{'Name':'Kitchen','openPaths':(16,17)},
	16:{'Name':'Attic','openPaths':(15,)},
	17:{'Name':'Living Room','openPaths':()}
}

visited_paths=[0]*18
loop=False
win_index=False
name=''

app = Flask(__name__)

def start_point():
	return random.randint(0,5)

curr_index=start_point()

def check_visited(index):
	if(visited_paths[index]==0):
		return False
	else:
		return True

def mark_visited(index):
	visited_paths[index]=1

@app.route('/')
def home():
    global name
    name=''
    return render_template('home.html')

@app.route('/ingame')
def ingame():
    error=None
    global name
    global curr_index
    global visited_paths
    if 'Name' in request.args:
        name=request.args['Name']
        if(name==''):
            error='Please enter a valid name'
            return render_template('home.html',error=error)
        mark_visited(curr_index)
        return render_template('ingame.html',index=curr_index,map_dict=map_dict,error=error,name=name)
    else:
        try:
            next_move=int(request.args['nextMove'])
            if next_move not in map_dict[curr_index].get('openPaths'):
                raise ValueError
        except ValueError:
                error='Please enter only from the available options'
                return render_template('ingame.html',index=curr_index,map_dict=map_dict,error=error,name=name)
        else:
            if(next_move==17):
                visited_paths= [0]*18
                # name=''
                curr_index=start_point()
                return render_template('winner.html',name=name)
            loop=check_visited(next_move)
            if(loop==True):
                visited_paths= [0]*18
                # name=''
                loop=False
                curr_index=start_point()
                return render_template('gameover.html',name=name)
            else:
                curr_index=next_move
                mark_visited(next_move)
                error=None
                return render_template('ingame.html',index=next_move,map_dict=map_dict,error=error,name=name)
