import clang.cindex
import clang.enumerations

def processString(myString):
  processedString=myString.lower().replace(" ", "").replace("_", "")
  return processedString

def processToken(kind, spelling, names):
  if spelling in names: return names[spelling]
  if kind==clang.cindex.TokenKind.LITERAL: return "!!LIT"
  if kind==clang.cindex.TokenKind.IDENTIFIER:
    return processString(spelling)
  if kind==clang.cindex.TokenKind.COMMENT: return None
  return spelling

id=0
tokenDict={}
def traverse(cursor):
  global id
  thisId=id
  self_tokens = cursor.get_tokens()
  selfTokenList=[i.spelling for i in self_tokens]
  childTokenList = []
  uniqueTokens=[]
  for child in cursor.get_children():
    id+=1
    traverse(child)
    child_tokens=child.get_tokens()
    childTokenList.extend([i.spelling for i in child_tokens])
  j=0
  for i in selfTokenList:
    if j<len(childTokenList) and i == childTokenList[j]:
      j+=1
    else: 
      uniqueTokens.append(i)
  tokenDict[thisId]=uniqueTokens

def print_traversal(cursor, depth=0):
  print(depth*"    ", end='')
  print(cursor.kind.name)
  for child in cursor.get_children():
    print_traversal(child, depth+1)


def processSource(source):
  index = clang.cindex.Index.create()
  with open("temp/temp.cpp", "w") as outfile:
    outfile.write(source)
  tu=index.parse("temp/temp.cpp", args=["-fno-delayed-template-parsing"])
  root = tu.cursor
  print_traversal(root)