import sys as SYSTEM
SYSTEM.path.append('.')

from src.inf import env as ENV
from src import db
from src.reword import ReArrange

import tweepy 
import multiprocessing as MP
import time 

auth = tweepy.OAuthHandler(ENV.API_KEY, ENV.API_KEY_SECRET)
auth.set_access_token(ENV.ACCESS_TOKEN, ENV.ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)


def pull_timeline(screen_name:str,rts:bool)->None:
    # fetching the statuses  
    statuses = api.user_timeline(screen_name = screen_name,include_rts=rts)
    return statuses

def read_list():
    user_list_ = list()
    with open('bin/list.txt','r') as f:
        for i in f.readlines():
            for j in str(i).split():
                user_list_.append(j)
    ENV.user_list = user_list_
    return user_list_

def make_post(text:str)->None:
    api.update_status(text)
    return


def post_text_extracter(data):
    json = data._json
    text = json['text']
    return text

def Regroup_and_post(ScreenName:str,rts=True):
    make_post(ReArrange(post_text_extracter(pull_timeline(ScreenName)[0])))

def auto_caller(rts=True):
    while True:
        read_list() # read if there is ay update in list 
        print(ENV.user_list) 
        for user in ENV.user_list:
            #user time line 
            try:
                dataJson = pull_timeline(str(user),rts=False)[0]._json
                print(dataJson)

                dataBase = db.get_screen_list().to_dict() # the SQL data base retrive data in pandas data frame 

                screenNames = dataBase['screen_name']  # Screen Name of the user in the list that have been previously called 
                ScreenNameList = list() # that's the name list of the users 
                last_posted_ids = dataBase['last_posted']
                
                LastPostedList = list()

                for indexSN , ScreenName in screenNames.items():
                    print(ScreenName)
                    ScreenNameList.append(ScreenName)
                    
                for indexLPid , LPid in last_posted_ids.items():
                    LastPostedList.append(LPid)
                print(LastPostedList)
                if user in ScreenNameList:
                    if not str(dataJson['id_str']) in LastPostedList:
                        print('there was a new post')
                        print(str(LastPostedList[int(ScreenNameList.index(str(user)))]))
                        db.updateExisting(user,str(dataJson['id_str']))
                        time.sleep(3)
                        new_text = ReArrange(dataJson['text'])
                        if len(new_text) > 120:
                            new_text = new_text[0:119]                           
                        make_post(new_text)
                    else:
                        print('No new post is available')
                elif not user in ScreenName:
                    print('new user detected')
                    db.insert(user,str(dataJson['id_str']))


                print('timeline retirved')
                pass
            except:
                print('couldnot pull the timeline of the user')
                pass
              
        time.sleep(60) # sleep for 1 minute before the next call 
    
def auto_caller_initializer():
    p1 = MP.Process(target=auto_caller,args=(True,))
    p1.start()
    p1.join()
if __name__ == '__main__':    
    auto_caller_initializer()