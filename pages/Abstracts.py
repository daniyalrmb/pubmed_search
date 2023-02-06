# In most cases the abstract is divided into multiple paragraphs. This script separately extracts paragraphs for all 100 pubmed articles


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
  all_data = []
  for id in pubids:
    url = "https://pubmed.ncbi.nlm.nih.gov/"+ str(id)
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    l = []
    try:
      abstract_raw = soup.find('div', {'class': 'abstract-content selected'}).find_all('p')
      for item in abstract_raw:
        l.append(item.text)
    except:
      l.append("missing")
    all_data.append(l)
    
    dff = pd.DataFrame(all_data)
    dff = dff.iloc[dff.isnull().sum(axis=1).mul(1).argsort()]
    dff.columns =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    
    return dff
