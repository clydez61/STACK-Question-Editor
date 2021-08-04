#!/usr/bin/env python3

# qcreate: Copyright (C) 2020-2021 John C. Bowman
# Contributors: Julie Lew

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

VERSION='0.99rc8'

import os
import sys
import re
import argparse
import json
from subprocess import Popen,PIPE,call,run
from string import capwords
from lxml.etree import Element,SubElement,ElementTree,parse
from datetime import datetime
from slugify import slugify
from base64 import b64encode

forbiddenVariables=['integrate','next','from','diff','in','at','limit','sum','for','and','elseif','then','else','do','or','if','unless','product','while','thru','step']

forbiddenInputVariables=['q','columns','Columns']

nl='\n'

text=[
    'questiontext',
    'questionvariables',
    'questionnote',
    'prtcorrect',
    'prtpartiallycorrect',
    'prtincorrect',
    'generalfeedback',
    'specificfeedback',
    'feedbackvariables',
    'truefeedback',
    'falsefeedback',
    'hint',
    'tag'
]

nonotanswered=['radio','checkbox']

mc=nonotanswered.copy()
mc.append('dropdown')

mcfunctions="""
correct(A):=maplist(first,sublist(A,lambda([x],x[2])))$
check(a,A):=if listp(a) then is(a = correct(A)) else member(a,correct(A))$
mcq(A,[B]):=block([a,L,m,M],
if length(A) = 1 then L:append(A[1],B) else L:append([A],B),
m:length(L),
M:makelist(0,x,L),
for i:1 thru m do (
a:ascii(96+i),
M[i]:[a,L[i][2],sconcat("<b>(",a,")</b>"," ",L[i][1])]),M)$
shuffle([L]):=[random_permutation(L)]$
"""

reinput=re.compile(r'\[\[input:([A-Za-z0-9_]+)\]\]')
revalidation=re.compile(r'\[\[validation:([A-Za-z0-9_]+)\]\]')
refeedback=re.compile(r'\[\[feedback:([A-Za-z0-9_]+)\]\]')

def edits(data):
    return 'Any edits should be made to the original source: '+data+'\n'+'This question was generated with qcreate version '+VERSION+' from https://gitlab.com/stacktools/tools\n'

def jaxify(s):
    return re.sub(r'(?<!\\)%[^\n]*\n','',re.sub(r'(?<!{)(@[^}]*?@)','\g<1>',
                                                re.sub(r'(?<!\\)\$(.*?)(?<!\\)\$','\(\g<1>\)',
                                                       re.sub(r'(?<!\\)\$\$(.*?)\$\$(?<!\\)','\[\g<1>\]',s,flags=re.S),
                                                       flags=re.S))).replace(r'\\$','$').replace(r'\\%','%')

def unescape(s):
    return s.replace('\\','\\\\')

def stackify(s):
    return unescape('\n'+re.sub(r'[;$]\n','\n',re.sub(r'(?<![;$\n])\n',' ',s)))

def paragraphify(s):
    return s.replace('\n\n','\n<p>\n')

def stack(s):
    fin=open(s)
    return '\n'+jaxify(fin.read())

texdefs=''

def tex(s):
    global texdefs
    texdefs += stack(s)
    return '\n\('+stack(s).replace('\n\n','')+'\)\n'

def python(s):
    fin=open(s)
    return jaxify(unescape(fin.read()))

def load(s):
    fin=open(s)
    return fin.read()

def stripxml(s):
    return s.replace('<br>','').replace('<p>','').replace('</p>','').replace('\\"','"').replace('$','\\$').replace('%','\\%')

import stackDefaults

def indent(elem, level=0):
    i='\n'+level*'  '
    if len(elem):
        if not (elem.text and elem.text.strip()):
            elem.text=i+'  '
        if not (elem.tail and elem.tail.strip()):
            elem.tail=i
        for elem in elem:
            indent(elem,level+1)
        if not (elem.tail and elem.tail.strip()):
            elem.tail=i
    else:
        if level and not(elem.tail and elem.tail.strip()):
            elem.tail=i

def addtext(key,value):
    if isinstance(value,str) and key in text:
        return {'text': value}
    return value

def xmlfromdict(x,o,parent=None,parentKey=None):
    print(type(o))
    print(o)
    if isinstance(o,dict):
        if parent != None:
            e=SubElement(parent,parentKey)
        else:
            e=x
        for key,value in o.items():
            if key != 'text':
                value=addtext(key,value)

            xmlfromdict(e,value,e,key)
        if parent != None:
            x.append(e)
    elif isinstance(o,list):
        for value in o:
            value=addtext(parentKey,value)
            xmlfromdict(x,value,parent,parentKey)
    else:
        x=SubElement(parent,parentKey)
        x.text=str(o)

def openFile(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    else:
        opener ='open' if sys.platform == 'darwin' else 'xdg-open'
        call([opener,filename])

def replacevariables(texexpressions,texsplit,maclines):
    macexpressions=[]

    for match in re.finditer(r'TeX\((.+?)\)\n\$\$(.+?)\$\$',maclines,flags=re.S):
        macexpressions.append(re.sub(r'\n','',match.group(2)))

    if len(texexpressions) != len(macexpressions):
        print('Maxima error')
        if not args.m0:
            print('rerun with -m option')
        exit()

    # match each TeX variable with the corresponding maxima expression
    for i in range(len(texexpressions)):
        k=2*i+1
        if texsplit[k] != '@':
            texsplit[k]=re.sub('!BOOLTRUE!','true',
                                   re.sub('!BOOLFALSE!','false',
                                          re.sub('!AND!','and',
                                                 re.sub('!OR!','or',
                                                        macexpressions[i]))))
    return ''.join(texsplit)

P=argparse.ArgumentParser(description='Create Moodle Stack XML question from Python source.')
P.add_argument('-u',metavar='ccid',help='Author ID')
P.add_argument('-o',metavar='outdir',help='Output directory')
P.add_argument('-t',action='store_true',help='Test LaTeX code')
P.add_argument('-m',action='store_true',help='Test Maxima code')
P.add_argument('-s', action = 'store_true', help='Add solutions')
P.add_argument('source',nargs='+')
args=P.parse_args()

args.t0=args.t
args.m0=args.m

if args.s:
    args.m=True
    args.t=True

CCID=args.u

if CCID == None:
    CCID=os.getenv('USER')

if CCID == None:
    CCID = ''
else:
    CCID += '-'

start=int(datetime.now().timestamp())

for data in args.source:
    root=Element('quiz')
    child=SubElement(root,'question',type='stack')

    options=stackDefaults.options.copy()
    input=stackDefaults.input.copy()
    prt=stackDefaults.prt.copy()
    node=stackDefaults.node.copy()
    hint=stackDefaults.hint.copy()
    hints=stackDefaults.hints

    initmc=True
    texdefs=''

    prefix=data.replace('.py','')
    data=prefix+'.py'
    prefix=os.path.basename(prefix)
    canonicalName=capwords(prefix.replace('-',' '))
    fin = open(data, 'r').read()
    exec(fin)
    #fin=open(data)
    #exec(jaxify(unescape(fin.read())))

    if args.m:
        macname=data.replace('.py','')+'.mac'
        if sys.platform == 'win32':
            macname=macname.replace('\\','/')
        macout=open(macname,'w')
        macout.write('load("operatingsystem")$\n')
        macout.write('chdir("stack/stack/maxima")$\n')
        macout.write('load("stackmaxima.mac")$\n')
        macout.write('display2d:true$\n')
        macout.write('linel:79$\n')
        macout.write('set_tex_environment_default("","")$\n')
        macout.write('TeX(L):=(print("$$"),if listp(L) and length(L) > 1 and listp(L[1]) then block([n:length(L)], for i:1 thru n do (sprint("\\\\\\\\"), tex(L[i]))) else (sprint("{"),tex(L),sprint("}")),print("$$"))$\n')

    if 'questionvariables' not in question:
        question['questionvariables']=''

    if 'input' not in question:
        question['input']=[]

    Input=question['input']
    if not isinstance(Input,list):
        Input=[Input]

    if 'prt' not in question:
        question['prt']=[{}]

    Prt=question['prt']
    if not isinstance(Prt,list):
        Prt=[Prt]

    if 'name' in question:
        qname=question['name']
    else:
        qname=canonicalName

    question['name']={
        'text': qname
    }

    filename=slugify(qname+'-'+CCID)+'.xml'

    outdir=args.o
    if outdir != None:
        if outdir[len(outdir)-1] != os.sep:
            outdir += os.sep

        filename=outdir+filename

    try:
        tree=parse(filename)
        Root=tree.getroot()
        for Child in Root:
            if Child.attrib['type'] != 'category':
                id=Child.find('idnumber').text
    except:
        id=CCID+str(datetime.fromtimestamp(start).strftime('%F-%H-%M'))
        start += 60

    question['idnumber']=id
    suffix=' id='+id

    for key,value in options.items():
        if key not in question:
            question[key]=str(value)

    a=question['questiontext'].split('[[input:')
    v=question['questiontext'].split('[[validation:')
    f=question['questiontext'].split('[[image:')

    validation=[]
    for k in range(1,len(v)):
        validation.append(v[k].split(']]')[0].strip())

    files=[]
    for k in range(1,len(f)):
        name=f[k].split(']]')[0].strip()
        files.append(name)
        question['questiontext']=question['questiontext'].replace('[[image:'+name+']]','<img src="@@PLUGINFILE@@/'+os.path.basename(name)+'">')

    afterinput=options['validation'] == 'afterinput'

    lastname=''
    for k in range(1,len(a)):
        rawname=a[k].split(']]')[0]
        name=rawname.strip()
        if afterinput and name not in validation:
            question['questiontext']=question['questiontext'].replace('[[input:'+rawname+']]','[[input:'+name+']][[validation:'+name+']]')
        if name in forbiddenInputVariables:
            print('Forbidden input variable: '+name)
            exit()

        missing=True
        Missing=True
        matrix0='matrix([0]);'
        if input['type'] == 'matrix':
            v=matrix0
        else :
            v='0;'

        Name=''
        Variable=stackDefaults.modelAnswer(name)
        for i in Input:
            if i['name'] == name:
                missing=False
                if 'tans' in i:
                    Missing=False
                    Name=i['tans']
                if 'type' in i and i['type'] == 'matrix':
                    v=matrix0
                break
        if missing or Missing:
            Name=Variable
            if missing:
                Input.append({
                    'name': name,
                    'tans': Name
                })
            else:
                i['tans']=Name

        if Name in forbiddenVariables:
            print('Forbidden question variable: '+Name)
            exit()
        if Variable not in question['questionvariables'].strip():
            question['questionvariables'] += Variable+':'+v+'\n'

    for i in Input:
        name=i['name']
        if 'tans' not in i:
            i['tans']=stackDefaults.modelAnswer(name)
        if 'type' in i and i['type'] in nonotanswered and 'options' not in i:
            i['options']='nonotanswered'

        if 'type' in i and i['type'] in mc and initmc:
            question['questiontext'] += '\(\)'+nl
            question['questionvariables']=mcfunctions+question['questionvariables']
            initmc=False

        if not afterinput and name not in validation:
            question['questiontext'] += '\n[[validation:'+name+']]\n'

        missing=True
        for p in Prt:
            if 'node' in p:
                nodes=p['node']
                if not isinstance(nodes,list):
                    nodes=[nodes]
                for n in nodes:
                    if ('sans' in n and n['sans'] == name) or ('name' in n and n['name'] == name) or ('input' in n and n['input'] == name):
                        if 'tans' not in n:
                            n['tans']=i['tans']

                        missing=False
                        break

        MC='type' in i and i['type'] in mc
        if MC and 'showvalidation' not in i:
            i['showvalidation']='0'

        if 'graded' in i:
            if not i['graded']:
                missing=False

            del i['graded']

        # Handle inputs that have no associated prt node
        if missing:
            tans=i['tans']
            if MC:
                sans='check('+name+','+tans+')'
                tans='true'
            else:
                sans=name

            if options['grading'] != 'manual':
                index=0
                def check(q,j):
                    global index
                    if 'name' in q:
                        if q['name'] == lastname:
                            index=j+1
                            # Determine best position to insert missing node
                for j in range(0,len(Prt)):
                    Q=Prt[j]
                    if 'node' in Q:
                        Q=Q['node']
                    if isinstance(Q,list):
                        for q in Q:
                            check(q,j)
                    else:
                        check(Q,j)

                Prt.insert(index,{
                    'name': name,
                    'node': {
                        'name': name,
                        'sans': sans,
                        'tans': tans,
                    }
                })

        lastname=name

        for key,value in input.items():
            if key not in i:
                i[key]=str(value)

        if i['showvalidation'] == '0':
            i['mustverify']='0'

    question['questiontext']=paragraphify(question['questiontext'])

    maxima=question['questionvariables']
    if args.m:
        macout.write(maxima.replace('\\','\\\\')+nl+nl)
        for i in Input:
            if 'type' in i and i['type'] in mc:
                answer='correct('+i['tans']+')'
            else:
                answer=i['tans']

            macout.write(i['name']+':'+answer+'$'+nl)

    if ';' in maxima or '$' in maxima:
        question['questionvariables']=stackify(maxima)

    if 'specificfeedback' not in question:
        question['specificfeedback']=''

    # Remove unused prts
    Prt0=[]
    for p in Prt:
        if 'node' in p:
            Prt0.append(p)

    maxgrade=0
    prtcount=1
    for p in Prt0:
        if 'name' not in p:
            p['name']='prt'+str(prtcount)

        prtcount += 1
        if 'feedbackvariables' in p:
            feedback=p['feedbackvariables']
            if args.m:
                macout.write(feedback)
            if ';' in feedback:
                p['feedbackvariables']=stackify(feedback)

        feedback='[[feedback:'+p['name']+']]'
        if feedback not in question['questiontext'] and feedback not in question['specificfeedback']:
            question['specificfeedback'] += feedback+'\n'

        for key,value in prt.items():
            if key not in p:
                p[key]=str(value)

        count=0

        nodes=p['node']
        if not isinstance(nodes,list):
            nodes=[nodes]

        length=len(nodes)
        if length > stackDefaults.maxNodes:
            print('Stack cannot handle more than '+str(stackDefaults.maxNodes)+' nodes')
            exit()

        maxgrade += length
        if length > 0:
            defaultscore=1/length
        else:
            defaultscore=0

        p['value']=length
        for n in nodes:
            if 'input' in n:
                del n['input']
            if 'name' in n:
                common=str(n['name'])
                if 'sans' not in n:
                    n['sans']=common
            else:
                common=n['sans']

            n['name']=count
            count += 1
            name=p['name']
            if args.m:
                macout.write('is(equal('+n['sans']+','+n['tans']+'));'+nl)

            n['trueanswernote']=name+'-'+str(count)+'-T'
            n['falseanswernote']=name+'-'+str(count)+'-F'

            if 'truescore' not in n:
                n['truescore']=defaultscore

            if 'truenextnode' not in n:
                if count < length:
                    n['truenextnode']=count

            if options['grading'] != 'elimination' and 'falsenextnode' not in n:
                if count < length:
                    n['falsenextnode']=count

            if 'truefeedback' in n:
                n['truefeedback']=paragraphify(n['truefeedback'])
            elif not common.isdigit():
                n['truefeedback']='<p>'+common+': correct</p>'

            if 'falsefeedback' in n:
                n['falsefeedback']=paragraphify(n['falsefeedback'])
            elif not common.isdigit():
                s='<p>'+common+': incorrect'
                if options['grading'] == 'elimination':
                    s += '; nothing further is graded'

                n['falsefeedback']=s+'</p>'

            for key,value in node.items():
                if key not in n:
                    n[key]=str(value)

    if 'defaultgrade' not in question:
        question['defaultgrade']=maxgrade

    if 'questionnote' in question:
        note=question['questionnote']
        if note != '' and note[len(note)-1] != '\n':
            note += '\n'
    else:
        note=''

    question['prt']=Prt0
    question['questionnote']=note+edits(data)

    if 'hint' not in question:
        question['hint']=hint

    texexpressions=[]

    if args.t:
        texname=prefix+'.tex'
        texout=open(texname,'w')
        texout.write("""\\documentclass[12pt]{article}
\\usepackage{amsmath,amssymb,graphicx}
\\begin{document}
""")
        texout.write(texdefs)
        texlines=stripxml(question['questiontext'])
        if 'generalfeedback' in question:
            texlines += stripxml(question['generalfeedback'])

        answer=[]
        replace=[]
        for match in reinput.finditer(texlines):
            replace.append(re.escape(match.group(0)))
            answer.append(match.group(1))

        if args.s:
            # replace with ${@_ans@}$
            solution=['$@'+stackDefaults.modelAnswer(ans)+'@$' for ans in answer]
            for j in range(len(replace)):
                texlines=re.sub(replace[j],solution[j],texlines)

        texlines=re.sub(refeedback,'',re.sub(revalidation,'',texlines))
        texlines=re.sub(r'<img src="@@PLUGINFILE@@/([^."]+).*">',r'\\includegraphics{\g<1>}',texlines)

        texsplit=texlines.split('@')
        for i in range(1,len(texsplit),2):
            exp=texsplit[i]
            if exp == '': # map @@ to @
                exp='@'
            texsplit[i]=exp
            texexpressions.append(exp)

    protect=''
    textsplit=question['questiontext'].split('@')
    n=len(textsplit)
    for i in range(0,n-1,2):
        arg=textsplit[i+1]
        if arg == '':
            protect += textsplit[i]+'@'
        else:
            protect += textsplit[i]+'{@'+arg+'@}'
    if n % 2 == 1:
        question['questiontext']=protect+textsplit[n-1]

    xmlfromdict(child,question)
    qt=child.find('questiontext')
    for f in files:
        e=SubElement(qt,'file')
        e.attrib['name']=os.path.basename(f)
        e.attrib['path']=os.sep
        e.attrib['encoding']='base64'
        e.text=b64encode(open(f).read().encode('utf-8'))

    indent(root)

    ElementTree(root).write(filename)
    print(filename+suffix)

    maclines=''
    if args.m:
        for name in texexpressions:
            if name == '@':
                name='""'
            macout.write('TeX('+name+')$\n')

        macout.close()
        suffix='.bat' if sys.platform == 'win32' else ''
        maclines=run(['maxima'+suffix,'-b',macname],capture_output=True).stdout.decode()
        if args.m0:
            print(maclines)

    if args.t:
        if args.m:
            texlines=replacevariables(texexpressions,texsplit,maclines)
        texlines=re.sub(r'<b>(.*?)</b>',r'{\\bf \g<1>}',
                        re.sub(r'<i>(.*?)</i>',r'\\emph{\g<1>}',texlines,flags=re.S),flags=re.S)


        texout.write(texlines)
        texout.write("""\\end{document}
""")
        texout.close()

    if args.t0:
        os.system('pdflatex'+' '+texname)
        openFile(prefix+'.pdf')
