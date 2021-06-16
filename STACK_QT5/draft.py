import re 
SearchMe = "wow hello there i dotn think why there are so many [[input:ans1]], and [[input:ans2]],[[input:ans3]],[[input:ans3]],[[input:ans3]],[[input:ans3]],[[input:ans3]],[[input:ans3]]"



inputs = re.findall(r'\[\[input:[a-zA-z0-9]+', SearchMe) 
i=0

'''if len(inputs) < 6:   
  for index, elem in enumerate(inputs):
    print(index, elem)'''

for index, elem in enumerate(inputs):  
  rows, lastrow = divmod(index, 4)
  #self.addInput(0,index)
  print(rows,lastrow)
'index = 7'


'''row = 0
lastrow = 2
length = 4
for i in range(row):
  for j in range(length):
      
    print(i,j)'''


