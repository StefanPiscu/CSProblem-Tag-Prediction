import utils
with open("temp/temp.cpp", "r") as infile:
  source = infile.read()
processed = utils.processSource(source)
for node in processed:
  print(node)