from flask import Flask, request, abort
import random
from datetime import datetime
import requests

class Candidate:
    def __init__(self,Name):
        self.name = Name;
        self.up= 1;
        self.down= 0;
        
    def voteUp(self):
        self.up += 1;

    def voteDown(self):
        self.down += 1;

class RankList:
    def __init__(self, Name,Id):
        self.info = {}
        self.info['id'] = Id 
        self.info['name'] = Name
        self.info['createTime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
        self.info['activeTime'] = self.info['createTime'] 
        self.info['optionCount'] = 0 
        self.info['tags'] = {} 
        self.candidates = {}

    def setId(self,Id):
        self.info['id'] = Id

    def addTag(self,tag):
        self.info['tags'][tag] = 0

    def addCandidate(self,candidate):
        if candidate in self.candidates:
            return
        self.candidates[candidate] = Candidate(candidate)

def getMaxId(lists):
    maximum = -1 
    for key in lists.keys():
        if int(key) > maximum:
            maximum = int(key)
    return maximum
        
lists = {}
for i in range(0,100):
    lists[str(i)] = RankList("test"+str(i),str(i))
    for j in range(0,30):
        lists[str(i)].addCandidate('cand-'+str(i)+'-'+str(j))
        lists[str(i)].candidates['cand-'+str(i)+'-'+str(j)].up = random.randrange(0,2000)

        lists[str(i)].candidates['cand-'+str(i)+'-'+str(j)].down= random.randrange(0,800)


app = Flask(__name__)

@app.route('/api/ranklists', methods=['GET','POST'])
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
        return {"lists":rlists}
    if request.method == 'POST':
        pName = request.form.get('name')
        print(pName)
        mId = getMaxId(lists)
        lists[str(mId+1)] = RankList(pName,str(mId+1))
        return {'name':pName} 

@app.route('/api/ranklists/<Id>',methods = ['GET'])
def rankId(Id):
    if request.method == 'GET':
        if Id in lists.keys():
            return {'id':Id, 'name':lists[Id].info['name']}
        else:
            abort(404)

@app.route('/api/ranklists/<Id>/candidates',methods = ['GET','POST'])
def candidates(Id):
    if request.method == 'GET':
        rCandidates = []
        rlimit = request.args.get('limit')
        for key in lists[Id].candidates.keys():
            rCandidates.append({'name':key,'voteUp':lists[Id].candidates[key].up,'voteDown':lists[Id].candidates[key].down})
        if rlimit!=None:
            rCandidates = rCandidates[0:int(rlimit)]
        return {"candidates":rCandidates}


