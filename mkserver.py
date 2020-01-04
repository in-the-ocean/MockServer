from flask import Flask, request, abort
from randomtimestamp import randomtimestamp
import random
from datetime import datetime
import requests

NOUNS = ['teacher','GE course','CS course','HIST course','Chinese Restaurant','Restaurant', 'city']

ADJS = ['Best','Worst']


class Candidate:
    def __init__(self,Name,cid):
        self.name = Name
        self.votes = {}
        self.cid = cid
        self.up= 0
        self.down= 0
        
    def voteUp(self,uid):
        if uid in self.votes:
            if self.votes[uid] == "up":
                return
            else:
                self.down-=1
        self.votes[uid] = "up"
        self.up += 1;

    def voteDown(self,uid):
        if uid in self.votes:
            if self.votes[uid] == "down":
                return
            else:
                self.up-=1
        self.votes[uid] = "down"
        self.down += 1;

    def setCid(self,cid):
        self.cid = cid

class RankList:
    def __init__(self, Name, Id):
        self.info = {}
        self.info['id'] = Id 
        self.info['name'] = Name
        self.info['createTime'] = randomtimestamp(2010,False) 
        self.info['activeTime'] = randomtimestamp(self.info['createTime'].year,False)
        self.info['optionCount'] = 0 
        self.info['tags'] = {} 
        self.candidates = {}

    def setId(self,Id):
        self.info['id'] = Id

    def addTag(self,tag):
        self.info['tags'][tag] = 0

    def addCandidate(self,candidate,cid):
        for key in self.candidates.keys():
            if candidate == self.candidates[key].name:
                return
        self.candidates[cid] = Candidate(candidate,str(cid))
        self.info['optionCount']+=1

    def setCreateTime(self,time):
        self.info['createTime'] = time

    def setActiveTime(self,time):
        self.info['activeTime'] = time

def getMaxId(Dict):
    maximum =-1 
    for key in Dict.keys():
        if key > maximum:
            maximum = key
    return maximum
        
lists = {}
for i in range(0,100):
    listName = 'test'+str(i)
    lists[i] = RankList(listName,str(i))
    candNum = random.randrange(5,50,1)
    for j in range(0,candNum):
        candName = 'cand-'+str(i)+'-'+str(j)
        lists[i].addCandidate(candName,j)
        #lists[str(i)].candidates[str(j)].up = random.randrange(0,2000)
        #lists[str(i)].candidates[str(j)].down= random.randrange(0,800)

'''
users = {}
for i in range(0,100):
    users[i] = {}
    for key in lists.keys():
        users[i][key] = {}
        for cand in lists[key].candidates.keys():
            myVote = random.choice(['up','down','up',None])
            if myVote != None:
                users[i][key][cand] = myVote
                if myVote == 'up':
                    lists[key].candidates[cand].voteUp()
                elif myVote == 'down':
                    lists[key].candidates[cand].voteDown()

print(users)
'''         
users = []
for i in range(0,100):
    users.append(i)
for lst in lists.keys():
    for cand in lists[lst].candidates.keys():
        for user in random.sample(users,random.randrange(0,80)):
            vote = random.choice(['up','up','down'])
            if vote == 'up':
                lists[lst].candidates[cand].voteUp(user)
            else:
                lists[lst].candidates[cand].voteDown(user)

    


app = Flask(__name__)

@app.route('/api/ranklists', methods=['GET','PUT'])
def ranklists():
    if request.method == 'GET':
        rlists = []
        rName = request.args.get('name')
        rtags = request.args.get('tag')
        rlimit = request.args.get('limit')
        for key in lists.keys():
            if rName!=None:
                if lists[key].info['name'] == rName:
                    rlists.append(lists[key].info)
            else:
                rlists.append(lists[key].info)
        if rlimit != None:
            rlists = rlists[0:int(rlimit)]
        return {"lists":rlists},200
    if request.method == 'PUT':
        pName = request.form.get('name')
        for key in lists.keys():
            if lists[key].info['name'] == pName:
                return {}
        mId = getMaxId(lists)
        lists[mId+1] = RankList(pName, str(mId+1))
        lists[mId+1].setCreateTime(datetime.now())
        lists[mId+1].setActiveTime(datetime.now())
        return {} 

@app.route('/api/ranklists/<Id>',methods = ['GET'])
def rankId(Id):
    if request.method == 'GET':
        if int(Id) in lists.keys():
            return {'id':Id, 'name':lists[int(Id)].info['name']}
        else:
            abort(404)

@app.route('/api/ranklists/<Id>/candidates',methods = ['GET','PUT'])
def candidates(Id):
    if request.method == 'GET':
        rCandidates = []
        rlimit = request.args.get('limit')
        rUid = request.args.get('uid')
        print(int(Id))
        if int(Id) not in lists:
            abort(404)
        for key in lists[int(Id)].candidates.keys():
            myVote = "None"
            if rUid != None and int(rUid) in lists[int(Id)].candidates[key].votes:
                myVote = lists[int(Id)].candidates[key].votes[int(rUid)] 
            rCandidates.append({'name':lists[int(Id)].candidates[key].name,
                                'cid':lists[int(Id)].candidates[key].cid,
                                'voteUp':lists[int(Id)].candidates[key].up,
                                'voteDown':lists[int(Id)].candidates[key].down,
                                'myVote':myVote})
        if rlimit!=None:
            rCandidates = rCandidates[0:int(rlimit)]
        return {"candidates":rCandidates}
    if request.method == 'PUT':
        cName = request.form.get('name')
        uid = request.form.get('uid')
        for key in lists[int(Id)].candidates.keys():
            if cName == lists[int(Id)].candidates[key].name:
                return {}
        mId = getMaxId(lists[int(Id)].candidates)
        lists[int(Id)].candidates[mId+1] = Candidate(cName,str(mId+1))
        lists[int(Id)].setActiveTime(datetime.now())
        return {}
'''
@app.route('/api/ranklists/<Id>/candidates/<cid>/vote',methods = ['PUT','DELETE'])
def vote(Id,cid):
'''








