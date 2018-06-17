import urllib
import urllib2
import lxml
import os

from bs4 import BeautifulSoup

# Heroes name
heroes = []

# Import the URL
BASE_URL = "https://www.icy-veins.com/heroes/talent-calculator"

# Get heroes name
page = urllib2.urlopen(BASE_URL)
soup = BeautifulSoup(page, 'lxml')
heroes_names = soup.select('.heroes-portraits > .hero-link')
for hero in heroes_names:
  name = hero.attrs['href'].split('/')[-1]
  heroes.append(name)

def getHeroes():
  path = os.path.join(os.getcwd(), 'talents')
  if not os.path.exists(path):
    os.makedirs(path)

  for hero in heroes:
    hero = hero.lower()
    url = BASE_URL + '/' + hero
    # Fetch the page
    page = urllib2.urlopen(url)

    # Parse the page
    soup = BeautifulSoup(page, 'lxml')

    ## Get hero portrait
    hero_portrait_url = soup.select_one('.hero-header > .hero-portrait').attrs['src']
    hero_portrait_url = "http:" + hero_portrait_url

    print "Getting " + hero_portrait_url

    hero_path = os.path.join(os.getcwd(), 'talents/' + hero)
    if not os.path.exists(hero_path):
      print 'Creating dir:' + hero_path
      os.makedirs(hero_path)

    urllib.urlretrieve(hero_portrait_url, os.path.join(hero_path, hero + "-portrait.jpg"))
    print "Saving" + hero + "-portrait.jpg"
    ## Get hero talents
    talents = soup.select('.hero-talents > .talent-line > img')
    for talent in talents:
      t_name = talent.attrs['id']
      t_url = "http:" + talent.attrs['src']
      urllib.urlretrieve(t_url, os.path.join(hero_path, hero + "-" + t_name + ".jpg"))
      print "Saving " + hero + "-" + t_name + ".jpg"

getHeroes()