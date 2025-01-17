from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import csv
import sys 

def AVScrape(csv_file):
	""" Grabs all the AV data from Pro-Football-Reference.com
	Submits the data to the inputted CSV file"""
	pre_url = "http://www.pro-football-reference.com/play-index/psl_finder.cgi?request=1&match=single&year_min=1994&year_max=2016&season_start=1&season_end=-1&age_min=0&age_max=0&pos=qb&pos=rb&pos=wr&pos=te&pos=e&pos=t&pos=g&pos=c&pos=ol&pos=dt&pos=de&pos=dl&pos=ilb&pos=olb&pos=lb&pos=cb&pos=s&pos=db&pos=k&pos=p&c1stat=choose&c1comp=gt&c2stat=choose&c2comp=gt&c3stat=choose&c3comp=gt&c4stat=choose&c4comp=gt&c5comp=choose&c5gtlt=lt&c6mult=1.0&c6comp=choose&order_by=av&draft=0&draft_year_min=1936&draft_year_max=2016&draft_slot_min=1&draft_slot_max=500&draft_pick_in_round=pick_overall&conference=any&draft_pos=qb&draft_pos=rb&draft_pos=wr&draft_pos=te&draft_pos=e&draft_pos=t&draft_pos=g&draft_pos=c&draft_pos=ol&draft_pos=dt&draft_pos=de&draft_pos=dl&draft_pos=ilb&draft_pos=olb&draft_pos=lb&draft_pos=cb&draft_pos=s&draft_pos=db&draft_pos=k&draft_pos=p&offset="	

	with open("newData.csv", "w", newline="") as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		#wr.writerow(['Rk', 'Player', 'URL', 'Year', 'Age', 'Draft', 'Tm',
		#	'Lg', 'G', 'GS', 'Yrs', 'PB', 'AP1', 'AV', 'Position'])
		for i in range(1,2):
			print(i)
			sys.stdout.flush() # make sure number is printed out in real time
			season_url = pre_url +str(100*i)
			pageScrape(season_url, wr)

def pageScrape(season_url, wr):
	""" Takes in a URL to a page of 100 AV options"""

	html = urlopen(season_url)
	soup = BeautifulSoup(html, "lxml")

	# our desired table has id = 'results'
	# we take the rows in the table's children
	# But we make sure to ignore the first two, since they're unrelated
	table = soup.find(id = 'results').findChildren("tr")[2:]
	soup.decompose()
	for elem in table:
		desired_row = []
		if not elem.has_attr('class'): # There are some rows we don't want
		# these rows have 'classes' while the ones we do want don't
			rank = int(elem.find('th').string)
			vals = elem.findAll('td')
			player = vals[0].a.string
			url = vals[0].a.get('href') 
			# url to the player's page on PFR
			# Used as a unique identifier for each player
			year = int(vals[1].string)
			age = 0 # some players don't have an age input
			if vals[2].string: 
				age = int(vals[2].string)
			draft = str(vals[3].string)
			tm = '2TM' # players who've played on two teams
			if vals[4].a:
				tm = vals[4].a.string
			lg = ""
			if vals[5].a:# some players don't have a league?
				lg = vals[5].a.string 
			g = 0
			if vals[6].string:
				g = int(vals[6].string)
			gs = 0
			if vals[7].string:
				gs = int(vals[7].string)
			yrs = int(vals[8].string)
			pb = int(vals[9].string)
			AP1 = int(vals[10].string)
			AV = int(vals[11].string)
			Position = getPosition(url, year)		

			# writing to file
			desired_row.extend((rank, player, url, year, age,
				draft, tm, lg, g, gs, yrs, pb, AP1, AV, Position))
			wr.writerow(desired_row)


def getPosition(player_url, year):
	'''Gets a player's position from his personal URL page'''
	print("player_url: " + player_url)
	base_url = "http://www.pro-football-reference.com"
	# Now we need to get each player's position
	html_player = urlopen(base_url + player_url)
	soup_player = BeautifulSoup(html_player, "lxml")

	# main table on page, showing stats for every year of the player's career
	year_table = soup_player.find('table')
	table_type = year_table.get('id') #table_type is either passing, defense, rushing_and_receing, etc.
	
	year_id = table_type+"."+ str(year)
	desired_row = soup_player.find(id= year_id)

	position = desired_row.find("td", {"data-stat":"pos"}).text

	soup_player.decompose()

	return position

	

# Url we will be scraping

AVScrape("../data/AVdata_with_position.csv")

