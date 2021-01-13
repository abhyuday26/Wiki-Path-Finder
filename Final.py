# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 12:06:41 2021

@author: abhyu
"""

import tkinter as tk
#from add import *

import xml.etree.ElementTree as ET
import mwparserfromhell
flag = 0
def addi(title_src,title_dest):
    global label5,label6,label7
    tree = ET.parse('E:\Mini Project\enwiki-latest-pages-articles_3_1.xml')
    rootx = tree.getroot()
    print(rootx.tag)
    #title_src=input('Enter source title:')
    #title_dest=input('Enter destination title:')
    #Aesthetics,Archimedes,Ant,Birds,Cicero
    global flag
    flag+=1
    flag_s=0
    flag_d=0
    #all title list
    i1=0
    alltitle=[]
    for pagex in rootx.iter('page') :
        alltitle.append(pagex.find('title').text)
        i1+=1
    pagex=None
    rootx=None
    #to find title_src
    if title_src in alltitle :
        flag_s=1
        print('Found title_src',title_src)
        label5 = tk.Label(root, text='Found Source Title')
        label5.config(font=('helvetica', 10))
        canvas1.create_window(300, 230, window=label5)
    else :
        print("Source title was not found!")
        label5 = tk.Label(root, text='Source Title Not Found')
        label5.config(font=('helvetica', 10))
        canvas1.create_window(300, 230, window=label5)
    #to find title_dest
    if title_dest in alltitle :
        flag_d=1
        print('Found title_dest',title_dest)
        label6 = tk.Label(root, text='Destination Title Found')
        label6.config(font=('helvetica', 10))
        canvas1.create_window(300, 250, window=label6)
    else :
        print("Destination title was not found!")
        label6 = tk.Label(root, text='Destination Title Not Found')
        label6.config(font=('helvetica', 10))
        canvas1.create_window(300, 250, window=label6)
    #finding
    from collections import defaultdict
    #arti_dict={}
    arti_dict = defaultdict(list)
    flag_found=0
    if flag_s==1 and flag_d==1 :
        #.
        L0=[]
        prev_ttl=None
        L1=[]
        L2=list()
        t3=None
        L0.append(title_src)
        tree = None
        #parsing the file again
        tree = ET.parse('E:\Mini Project\enwiki-latest-pages-articles_3_1.xml')
        root1=tree.getroot()
    
        #some counters
        counter=0
        cn=1
        level=0
    
        for ttl in L0 :
            if counter == cn :
                level+=1
                cn=newlength-1
                counter=0
                print('There aren\'t any matches in level',level)
                newlength=None
                label7 = tk.Label(root, text='There aren\'t any matches in level '+str(level))
                label7.config(font=('helvetica', 10))
                canvas1.create_window(300, 270, window=label7)
                #def input(s)
                #s=input('..If u want to continue choose \'y\', else to terminate choose \'n\':')
                #if s == 'n' or s != 'y' :
                 #   exit(0)
                if level < 4:    
                    answer = tk.messagebox.askquestion("Permission To Continue",
                                                       "Click Yes to continue click No to abort")
                else:
                    answer = tk.messagebox.askquestion("Permission To Continue",
                                                   "Click Yes to continue click No to abort"+'\n'+"Caution: It might take time")
 
                if answer == 'yes':
                    tk.messagebox.showinfo('','Processing')
                    
                    #root.destroy()
                else:
                    tk.messagebox.showinfo('', 'Aborting')
                    root.destroy()    
                    
                #if answer == 'no':
                    #root.destroy()
                    
                    
    
            for page2 in root1.findall('page') :
                t3=page2.find('title').text
                if t3==ttl :
                    L1.clear()
                    L2.clear()
                    wiki = mwparserfromhell.parse(page2.find('revision').find('text').text)
                    L2 = [x.title for x in wiki.filter_wikilinks()]
                    #check:to see if title_dest is contained in immediate wikilinks obtained in L1
                    if title_dest in L2 :
                        print('Great!...Path found at level',(level+1),'Here it is...')
                        ##print(L2.index(title_dest))
                        prev_ttl=ttl
                        flag_found=1
    
                    #filters
                    for link in L2 :
                        #filter:'File:'
                        if 'File:' in link :
                            continue
                        #filter:repetition in a page
                        if link in L1 :
                            continue
                        #filter:file size constraint
                        if link not in alltitle :
                            continue
                        #filter:already encountered previously
                        if link in L0 :
                            continue
                        else :
                            L1.append(link)
                    ##print(ttl,':',L1[:])
                    #break has to be applied in this if as u have found the titles wikilinks so to avoid useless multiple comparisons
    
                    #now assigning key values to dictionary
                    arti_dict[t3]=L1[:]
                    ##print(ttl,':',arti_dict[t3])
    
    
    
                    if flag_found==1 :
                        #break1
                        break
    
            #control comes here after break 1
    
            counter+=1
    
            #extending list L0
            L0.extend(L1)
            newlength=len(L0)
            ##print(L0[:])
            ##print(len(L0[:]))
    
            if flag_found==1 :
                #break2
                break
    
        #control comes here after break 2
    
    else :
        exit(0)
    
    if flag_found==0 :
        print('No path was found between the provided links')
        exit(0)
    
    #print(arti_dict)
    #print(prev_ttl)
    
    #path
    paths=list()
    paths.append(title_dest)
    ##print(paths[:])
    paths.append(prev_ttl)
    ##print(paths[:])
    
    def afunc(d,p) :
        flaggs=0
        for key in d :
            ##print(arti_dict[key])
            v=d[key]
            if p in v :
                p=key
                flaggs=1
                return p
        if not flaggs :
            return 'xxx'
    
    var=prev_ttl
    while var != title_src :
        var = afunc(arti_dict,prev_ttl)
        prev_ttl = var
        paths.append(var)
    paths.reverse()
    
    pa = ''
    for pp in paths :
        if paths.index(pp) < (len(paths)-1) :
            pa += str(pp) + " ==> "
        else :
            pa += str(pp)
    ##print(paths[:])
    return(pa)





root= tk.Tk()

canvas1 = tk.Canvas(root, width = 600, height = 380,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Find the path in wiki articles')
label1.config(font=('helvetica', 14))
canvas1.create_window(300, 25, window=label1)

label2 = tk.Label(root, text='Enter Source Title')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)

label21 = tk.Label(root, text='Enter Destination Title')
label21.config(font=('helvetica', 10))
canvas1.create_window(400, 100, window=label21)

entry11 = tk.Entry (root) 
canvas1.create_window(400, 140, window=entry11)


def getPath ():
    global label3,label4
    title_src = entry1.get()
    destination_src = entry11.get()
    path = addi(title_src,destination_src)
    if(flag>1):
        label3.destroy()
        label4.destroy()
        label5.destroy()
        label6.destroy()
        label7.destroy()
    #path = addi('Anarchism','Ant')

    label3 = tk.Label(root, text= 'The Path Between '+title_src +' and '+ destination_src + ' is:',font=('helvetica', 10))
    canvas1.create_window(300, 290, window=label3)
    #label3.destroy()    
    label4 = tk.Label(root, text= path,font=('lobster', 12, 'bold'))
    canvas1.create_window(300, 330, window=label4)
    
button1 = tk.Button(text='Get the Path', command=getPath, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(300, 180, window=button1)

root.mainloop()