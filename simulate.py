from flask import Flask,request,render_template,session,redirect,url_for,escape,Blueprint
import requests
import json
import sys
from cStringIO import StringIO

simulate_module = Blueprint('simulate_module', __name__)

var=[]
py=[]
lists=[]
py1=[]
errors=[]

countif=0
countloop=0
linecount=0


@simulate_module.route('/simulate', methods=['POST'])
def on_run():
	code = request.form['code']
	inp = request.form['input']
	out = exec_code(code,inp)
	ret = ()
	ret[0] = 'success'
	if(out[0] == 0):
		ret[0] = 'error'
		out[1] = '<br>'.join(out[1])
	ret[1] = out[1]
	return ret


def exec_code(code,inp):
	py.append(tabcount()+'import time')
	py.append('\n')
	py.append(tabcount()+'timeout= time.time() + 30')
	py.append('\n')
	py.append('starttime=time.time()')
	py.append('\n')

	listl = [x.strip() for x in code.strip().split('\n') if x]

	for k in range(len(listl)):
		statement = listl[k].split(' ')
		check(statement)

	if(countif>0):
		errors.append('Error in endif statement')

	if(countloop>0):
		errors.append('Error in endloop statement')

	py.append('endtime=time.time()')
	py.append('\n')
	py.append('Runtime=-starttime+endtime')
	py.append('\n')
	py.append('print "Runtime: " + str(Runtime)')
	py.append('\n')

	py=''.join(py)

	if(len(errors)):
		return (0,errors)

	else:
		s = StringIO()
		old_stdout = sys.stdout
		sys.stdout = s
		#try-catch block
		exec(py)
		# catch output in error_python
		sys.stdout = old_stdout
		output = s.getvalue()
		if(error_python):
			return (error_python,0)
		else:
			return (output,1)

def breaks():
	m=py[:]
	global countif
	global countloop
	for i in range(len(py)):
		key=m.pop()
		key=key.split(' ')
		if(key[0]=="if"):
			countif-=1
		if(key[0]=="loop"):
			countloop-=1
			break

def tabcount(offset=0):
	if((countif+countloop+offset)>=1):
		k=''
		for i in range((countif+countloop)+offset):
			k+='\t'
		return k
	else:
		return ''

# var x; var x = 2
def makevar(x1, v=0):
	flag=0
	for i in range(len(var)):
				if(x1==var[i]):
					errors.append('Multiple declaration of the same variable')
					flag=1
	if(flag==0):
		var.append(x1)
		py.append(tabcount()+x1+'='+v)
		py.append('\n')

# if statement
def eif(l):
	global countif
	py.append(tabcount()+l+':')
	py.append('\n')
	countif+=1

# else
def eelse():
	py.append(tabcount(-1)+'else:')
	py.append('\n')

#endif    
def endif():
	global countif
	countif-=1

#print
def eprint(c):
	py.append(tabcount()+'print '+c)
	py.append('\n')

#loop condition
def loop(m):
	global countloop
	py.append(tabcount()+'flagloop=0')
	py.append('\n')
	py.append(tabcount()+'while '+m+':')
	py.append('\n')
	countloop+=1
	
#endloop
def endloop():
	global countloop
	py.append(tabcount()+'if time.time()>timeout:')
	py.append('\n')
	py.append(tabcount(+1)+'flagloop=1')
	py.append('\n')
	py.append(tabcount(+1)+'break')
	py.append('\n')
	py.append(tabcount(-1)+'if flagloop==1:')
	py.append('\n')
	py.append(tabcount()+'print "Timeout"')
	py.append('\n')
	countloop-=1

#list name = ()
def makelist(ln, r):
	flagl=0
	for i in range(len(lists)):
		if(ln==lists[i]):
			errors.append('Multiple declaration of the same list')
			flagl=1
			
	if(flagl==0):
		py.append(tabcount()+ln+'='+r)
		py.append('\n')
		lists.append(ln)

#sort listname  
def sort(k=[]):
	py.append(tabcount()+k+'.sort()')
	py.append('\n')

def makearr(l):
	strt=l.index('[')
	end=l.index(']')
	ln=l[0:strt]
	val=l[strt+1:end]
	lists.append(ln)
	if(val.isdigit()):
		py.append(tabcount()+'strt= '+str(strt))
		py.append('\n')
		py.append(tabcount()+'end= '+str(end))
		py.append('\n')
		py.append(tabcount()+ln+'=[]')
		py.append('\n')
		py.append(tabcount()+'for i in range('+val+'):')
		py.append('\n')
		py.append(tabcount(+1)+ln+'.append(0)')
		py.append('\n')

	else:
		flagn=0
		for i in range(len(var)):
			if(val==var[i]):
				flagn=1
		if(flagn==1):
			py.append(tabcount()+'strt= '+str(strt))
			py.append('\n')
			py.append(tabcount()+'end= '+str(end))
			py.append('\n')
			py.append(tabcount()+ln+'=[]')
			py.append('\n')
			py.append(tabcount()+'for i in range('+val+'):')
			py.append('\n')
			py.append(tabcount(+1)+ln+'.append(0)')
			py.append('\n')

		elif(flagn==0):
			errors.append('Error in array declaration')

def check(l=[]):
	global linecount
	linecount+=1
	if(l[0]=="var"):
		if(len(l)== 4 or len(l) == 2):
			if(len(l)==4):
				makevar(l[1], l[3])

			if(len(l)==2):
				var.append(l[1])
			
		else:
			errors.append('Error in line '+ str(linecount))

	elif(l[0]=="if"):
		l=' '.join(l)
		eif(l)

	elif(l[0]=="endif"):
		endif()

	elif(l[0]=="else"):
		eelse()
		if(countif==0):
			errors.append('Error in else statement')

	elif(l[0]=="loop"):
		# print ("in loop")
		k=' '.join(l[1:])
		loop(k)
	#arr 2 = arr 3
	elif(l[0]=="arr"):
		if(len(l)==2):
			makearr(l[1])
		elif(len(l)==5):
			if(lists.count(l[1])>0 and lists.count(l[4])>0):
				py.append(l[1]+'='+l[4]+'[:]')
				py.append('\n')
			else:
				errors.append("Array doesn't exist")

	elif(l[0]=="sort"):
		sort(l[1])

	elif(l[0]=="print"):
		l=' '.join(l[1:])
		eprint(l)

	elif(l[0]=="endloop"):
		endloop()
		
	elif(l[0]=="break"):
		if(countloop==0):
			errors.append("No loop to break")
		else:
			py.append(tabcount()+'break')
			py.append('\n')
			breaks()
# input k; input arr k            
	elif(l[0]=="input"):
		if(len(l)==2):
			flagi=0
			for i in range(len(var)):
				if(l[1]==var[i]):
					flagi=1
			if(flagi==1):
				py.append(l[1]+'='+'input()')
				py.append('\n')
			elif(flagi==0):
				errors.append('Input variable does not exist')
			
		elif(len(l)==3):
			flagi=0
			for i in range(len(lists)):
				if(l[2]==lists[i]):
					flagi=1
			if(flagi==1):
				py.append(l[2]+'='+'raw_input()')
				py.append('\n')
				py.append(l[2]+'='+l[2]+'.split(' ')')
				py.append('\n')
				py.append(l[2]+'= map(int, '+l[2]+')')
				py.append('\n')
			else:
				errors.append('Array input variable does not exist')
# //                
	elif(l[0]=="//"):
		tc=' '.join(l[1:])
		py.append('# '+'tc')
		py.append('\n')
#elseif      
	elif(l[0]=="elseif"):
		if(countif==0):
			errors.append('Error in elseif statement')
		else:
			k=' '.join(l[1:])
			if(countif==0):
				errors.append("Error in elseif statement")
			elif(countif>0):
				py.append(tabcount(-1)+'elif '+k+':')
				py.append('\n')

	elif(l[0]=="string"):
		r=' '.join(l[1:])
		py.append(r)
		py.append('\n')
			
	else:
		k=' '.join(l)
		py.append(tabcount()+k)
		py.append('\n')