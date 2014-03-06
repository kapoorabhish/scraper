"""
this program searches the amazon.com from the text stored in the txt file viz. title and author(s) separated by tab.
and stores the result in a txt file.
"""
import requests
from bs4 import BeautifulSoup
from time import strftime,sleep,localtime



def search(title):
	
	info=[]
	url=requests.get('http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias&field-keywords=%s'%title ,headers={'User-agent':'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'})
	soup=BeautifulSoup(url.content)
	noRes=soup('span',{'class':'noResultsTitleKeyword'})
	if noRes==[]:
		res=soup('div',{'class':'fstRow'})
		for tag in res:
			if tag.text!="":
				info.append(tag.text.strip())
				break
		return info
	else:
		return

def search2(title):
	
	info=[]
	url=requests.get('http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias&field-keywords=%s'%title ,headers={'User-agent':'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'})
	soup=BeautifulSoup(url.content)
	noRes=soup('span',{'class':'noResultsTitleKeyword'})
	if noRes==[]:
		res=soup.find('div',{'class':'fstRow'})
		href=res.a['href']
		print href.split('/ref=')[0]
		url2=requests.get(href.split('/ref=')[0],headers={'User-agent':'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'})
		soup2=BeautifulSoup(url2.content)
		table=soup2('table')
		info.append(href)
		for each in table:
			x=each.find('div',{'class':'content'})
			try:
				li=x('li')
				for i in range(5):
					ret=li[i].text.split(':')
					if len(ret[0])<70 and len(ret[1])<70:
						info.append(','.join(ret))
			except:
				pass
		return info

	else:
		return


titles=open("titles_meds.txt","r")
searched=open("imported_details_%s.csv"%strftime("%d%m%Y%H%M%S",localtime()),'w')
print searched
proxy={'127.0.0.1':'8118'}
x=''
mrp=[]
temp=[]
offer=''
for line in titles:
	line=line.split('\t')
	t=line[1].strip().split(',')
	aut=t[0].replace(' ','+')
	s=line[0].strip().replace(' ','+')+'+'+'by'+'+'+aut
	try:

		temp=search(s)
		temp2=search2(s)
		x=[]
		for i in temp:
			x.append(i.replace('\n',''))
		#det=','.join()
		string = '"'+','.join(x)+'"'+','+','.join(temp2)+'\n'
		print string
	except:
		print 'error'
	searched.write(string.encode('UTF-8'))
	x=''
	temp=[]
	