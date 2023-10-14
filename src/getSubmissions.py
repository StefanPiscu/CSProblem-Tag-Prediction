import requests, time, json
from multiprocessing import Process, Pool
proxies = {
  "http" : "###########"
}


def fetchSource(submissionId):
    url = 'http://codeforces.com/data/submitSource'
    postdata = {'submissionId': submissionId}
    patience=10
    while True:
      res=requests.post(url, postdata, proxies=proxies)
      if patience==0 or res.status_code==200:
        break
      else:
        print(submissionId, res.status_code)
        patience-=1
        time.sleep(0.1)
    if res.status_code != 200:
      return None
    try:
      return res.json()["source"]
    except:
      return None

LANGUAGES = ["GNU C++20 (64)", "GNU C++17", "GNU C++14", "GNU C++17 (64)", "GNU C++11"]
def processSubmission(submission):
  if "verdict" not in submission or submission["verdict"]!="OK":
    return None
  if submission["programmingLanguage"] not in LANGUAGES:
    return None
  if submission["author"]["participantType"]!="CONTESTANT":
    return None
  if len(submission["author"]["members"])!=1:
    return None
  author=submission["author"]["members"][0]["handle"]
  mySubmission = {}
  mySubmission["author"]=author
  source=fetchSource(submission["id"])
  mySubmission["source"]=source
  return mySubmission

def fetchContestStatus(contestId):
  while True:
    res=requests.get(f"https://codeforces.com/api/contest.status?contestId={contestId}", proxies=proxies)
    if res.status_code==200 and res.json()["status"]=="OK":
      break
    else:
      print(f"FetchCountestStatus failure, code: {res.status_code}")
      time.sleep(0.1)
  return res.json()["result"]

def getAuthorData(authors):
  count=0
  crString=""
  authorData={}
  for handle in authors:
    count+=1
    crString+=handle+";"
    if count>500:
      while True:
        res=requests.get(f"https://codeforces.com/api/user.info?handles={crString}", proxies=proxies)
        if res.status_code==200 and res.json()["status"]=="OK":
          break
        else:
          print(res.status_code)
          time.sleep(0.1)
      count=0
      crString=""
      data=res.json()["result"]
      for user in data:
        handle=user["handle"]
        rating=-1
        if "rating" in user:
          rating=user["rating"]
        country = None
        if "country" in user: country=user["country"]
        authorData[handle]={"rating":rating, "country":country}
  if crString:
    while True:
      res=requests.get(f"https://codeforces.com/api/user.info?handles={crString}", proxies=proxies)
      if res.status_code==200 and res.json()["status"]=="OK":
        break
      else:
        print(res.status_code)
        time.sleep(0.1)
    data=res.json()["result"]
    for user in data:
      handle=user["handle"]
      rating=-1
      if "rating" in user:
       rating=user["rating"]
      country = None
      if "country" in user: country=user["country"]
      authorData[handle]={"rating":rating, "country":country}
  return authorData
  
def getSubmissionsFromContest(contestId):
  rawSubmissionList=fetchContestStatus(contestId)
  print(f"Got {len(rawSubmissionList)} Raw Submissions from contest {contestId}")
  submissionList=[]
  authors = set()
  nr=0
  last=0
  with Pool(12) as p:
    tempList=p.map(processSubmission, rawSubmissionList)
  for elem in tempList:
    if elem!=None:
      submissionList.append(elem)
      authors.add(elem["author"])

  print(f"Got {len(submissionList)} Processed Submissions from contest {contestId}")
  authorData=getAuthorData(authors)
  for i in range(len(submissionList)):
    author=submissionList[i]["author"]
    submissionList[i]["country"]=authorData[author]["country"]
    submissionList[i]["rating"]=authorData[author]["rating"] 
  return submissionList

def saveSubmissionsFromContest(contestId):
  with open(f"../submissions/{contestId}_submissions.json", "w") as outfile:
    outfile.write(json.dumps(getSubmissionsFromContest(contestId)))

if __name__ == '__main__':
  start_time=time.time()
  contestList = [1738]
  processes = [Process(target=saveSubmissionsFromContest, args=(id,)) for id in contestList]
  for process in processes:
    process.start()
  for process in processes:
    process.join()
  print("--- %s seconds" % (time.time()-start_time))


