"""
This program searches the mobile flipkart page by page and then fetches the details from the full site using the function goto_link()
And stores the result in a .txt file.

"""
from bs4 import BeautifulSoup
import requests
from time import sleep,strftime,localtime
from random import randint


def goto_link(link):
	sleep(randint(20,40))
	x=''
	other_edition=[]
	offer=''
	detail=[]
	mrp=''
	url=requests.get(link, headers={'User-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13'},proxies=proxy)
	soup=BeautifulSoup(url.content)
	search=soup.find('div', {'class':'asp-header no_results'})
	try:
		find=soup.find('div',{'class':'stock-status instock'})
		if find!=None:
			x=find.text.strip()[:-1]
			if x.split(' ')[0]=='Imported':
				isimported=True
		cost=soup.find('span',{'class':'price list price-td'})
		if cost!=None:
			mrp=cost.text[3:].strip()

		cost2=soup.find('span',{'class':'price final-price our fksk-our'})
		offer=cost2.text[3:].strip()
		table=soup.find('table',{'class':'fk-specs-type1'})
		td=table('td')
		for i in td:
			s=i.text.strip()
			detail.append(s)
	
	except :
		print 'error'

	temp=[]
	for i in detail:
		temp.append('"'+i+'"')

	det=','.join(temp)
	string=mrp+','+offer+','+det+'\n'
	print string
	return string







fklinks=open("links_%s.csv"%strftime("%d%Y%m%H%M%S",localtime()),'w')
print fklinks
sub='http://www.flipkart.com'
proxy={'127.0.0.1':'8118'}
details=[]
#sleep(randint(35,65)) 
for num in range(20,50):
	sleep(randint(20,50))
	url=requests.get("http://m.flipkart.com/m/academic-and-professional-books-5400/%d?__agent=mobile&layout=grid"%num, headers={'User-agent':'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'},proxies=proxy)
	soup=BeautifulSoup(url.content)

	print num
	link=soup('div',{'class':'imgpriceship'})
	for i in link:
		sublink=i.a['href']
		full=sub+sublink[2:]
		print full
		details=goto_link(full)
		fklinks.write((full+','+details).encode('UTF-8'))
