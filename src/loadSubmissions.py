import os, json

submissionList = []
files = ["../submissions/"+f for f in os.listdir('../submissions')]
for file in files:
  with open(file, 'r') as infile:
    submissionList.extend(json.load(infile))

