# enter the search url for pubmed search (displaying 100 results)
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import requests
from lxml import html
import time
from time import sleep
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as mp
nltk.download('stopwords')

def getData(search):
  url = "{}".format(search)
  tree = html.fromstring(requests.get(url).content)

# create an empty list for all 100 pubmed ids and run a loop to append all ids as integers to the empty list

  pubids = []
  i = 2
  for f in range(100):
    pubids.append( tree.xpath('/html/body/main/div[9]/div[2]/section/div[1]/div/div[{}]/article/header/div[1]/ul/li[1]/span/strong//text()'.format(str(i)) ))
    i = i+1
  pubids = [item for sublist in pubids for item in sublist]
  pubids = [int(x) for x in pubids]

# Using beautiful soup to scrape abstract, keywords, title, etc for all 100 pubmed articles

  
  abstract = []
  keywords = []
  title = []
  journal = []
  date = []
  authors = []
  affiliation = []
  for id in pubids:
    url = "https://pubmed.ncbi.nlm.nih.gov/"+ str(id)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, "lxml")
  # Get article abstract if exists - sometimes abstracts are not available (not an error)
  
    try:
      abstract_raw = soup.find('div', {'class': 'abstract-content selected'}).find_all('p')
  # Some articles are in a split background/objectives/method/results style, we need to join these paragraphs
      abstract.append(' '.join([paragraph.text.strip() for paragraph in abstract_raw]))
    except:
      abstract.append('NO_ABSTRACT')
  # Get article keywords - sometimes keywords are not available (not an error)
    try:
  # We need to check if the abstract section includes keywords or else we may get abstract text
      has_keywords = soup.find_all('strong',{'class':'sub-title'})[-1].text.strip()
      if has_keywords == 'Keywords:':
  # Taking last element in following line because occasionally this section includes text from abstract
        ks = soup.find('div', {'class':'abstract' }).find_all('p')[-1].get_text()
        keywords.append(ks.replace('Keywords:','\n').strip()) # Clean it up
      else:
        keywords.append('NO_KEYWORDS')
    except:
      keywords.append('NO_KEYWORDS')
    try:
      title.append(soup.find('meta',{'name':'citation_title'})['content'].strip('[]'))
    except:
      title.append('NO_TITLE')
    try:
      journal.append(soup.find('meta',{'name':'citation_journal_title'})['content'])
    except:
      journal.append('NO_JOURNAL')
    try:
      date.append(soup.find('time', {'class': 'citation-year'}).text)
    except:
      date.append('NO_DATE')
    autors = ''    # string because it's easy to split a string on ','
    try:
      for author in soup.find('div',{'class':'authors-list'}).find_all('a',{'class':'full-name'}):
        autors += author.text + ', '
                # alternative to get citation style authors (no first name e.g. I. Zenkov)
                # all_authors = soup.find('meta', {'name': 'citation_authors'})['content']
                # [authors.append(author) for author in all_authors.split(';')]
      authors.append(autors)
    except:
      authors.append('NO_AUTHOR')
  # Get author affiliations - sometimes affiliations are not available (not an error)
    afiliations = [] # list because it would be difficult to split since ',' exists within an affiliation
    try:
      all_affiliations = soup.find('ul', {'class':'item-list'}).find_all('li')
      for a in all_affiliations:
        afiliations.append(a.get_text().strip())
      affiliation.append(afiliations)
    except:
      affiliation.append('NO_AFFILIATIONS')
    
    # create a dataframe and add scraped data to appropriate column

  
  df = pd.DataFrame(list(zip(title, date, journal, keywords, authors, affiliation ,abstract )),
               columns =['Title', 'Date', 'Journal', 'Keywords', 'Authors', 'Affiliation', 'Abstract'])

  stop_words = set(stopwords.words('english'))
  out = df['Keywords'].str.split().explode().to_frame('Words')
  out['Words'] = out['Words'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in (stop_words)]))
  out = out[out["Words"].str.contains("NO_KEYWORDS") == False]
  out = out[out["Words"].str.contains("  ") == False]
  out = out.groupby('Words').size().reset_index(name='Count')
  out = out.sort_values('Count', ascending=False)

  # plot the dataframe
  out.iloc[1:10].plot(x="Words", y=["Count"], kind="bar", figsize=(9, 8))
  fig = mp.show()
  return df, fig
  
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

st.title("# Search PubMed for Dementia Studies! 🔎")

st.sidebar.success("Select an option above.")

search = st.text_input('Enter search URL')

if not search.startswith("http"):
  st.stop()

time.sleep(1)
p,g = getData(search)
csv = convert_df(p)
st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
time.sleep(1)

st.pyplot(g)

AgGrid(p, height=500, fit_columns_on_grid_load=True, enable_enterprise_modules=True)
