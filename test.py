import os
f= open ('ippool', 'r')
line = f.readlines()
a=os.popen("ping -n 10 www.baidu.com")  #使用a接收返回值
x = a.read()
print(x)

#for x in line:
#    message = 'ping '+ x
#    a = os.system(message)
#    print(a)