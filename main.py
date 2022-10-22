import pandas as pd
from usp.tree import sitemap_tree_for_homepage
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
from googlesearch import search
from progressbar import ProgressBar

# Wants the information as such:
# State, School, Abbreviation, Type (public/private/community), SGA email, size, SGA website (preferably with LINK hyperlink), notes (if using personal email or issue with contact methods)

# Function to determine if a url is valid
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Function to convert a url to a standard format
def standardize_url(url):
    if url[-1] == '/': url = url[:-1]
    url = 'https://www.' + url.strip().replace('http://', '').replace('https://', '').replace('www.', '')
    return url

# Importing the initial csv file
df = pd.read_csv('./us-colleges-and-universities.csv', encoding='UTF-8', on_bad_lines='skip', delimiter=';')

# Creating the dataframe to convert into a csv file
final_df = pd.DataFrame(columns=['State', 'School', 'Abbreviation', 'Type', 'Email', 'Size', 'Website', 'Address', 'Notes'])

# Setting shared columns to be the same in the final dataframe
final_df['State'] = df['STATE']
final_df['School'] = df['NAME'].str.title()
final_df['Size'] = df['TOT_ENROLL'].replace(-999, 'N/A')

# Creating the type column by mapping the number in the original csv file to a string
school_type = {1: 'Community', 2: 'Private', 3: 'Public'}
final_df['Type'] = df['TYPE'].map(school_type)

# Creating the abbreviation column by splitting the name column and taking the first letter of each word
articles = ['the', 'of', 'and', 'at', 'a', 'an', '&']
final_df['Abbreviation'] = [''.join(j[0] for j in x.split() if j.lower() not in articles) for x in final_df['School']]

# Creating the address column
final_df['Address'] = df['ADDRESS'].str.title() + ', ' + df['CITY'].str.title() + ', ' + df['STATE'].str.upper() + ' ' + df['ZIP'].astype(str)

# Getting all the SGA websites
pbar = ProgressBar()
sga_websites = []
for website in pbar(df['WEBSITE']):
    query = 'site:' + standardize_url(website) + ' student government association'
    sga_website = 'N/A'
    for url in search(query, lang='en', num=1, stop=1, pause=2):
        sga_website = standardize_url(url)
    sga_websites.append(sga_website)
final_df['Website'] = sga_websites

# Removing the rows that don't have a valid student government association website
final_df = final_df.loc[final_df['Website'] != 'N/A']

# Getting all the SGA emails
for website in final_df['Website']:
    email_list = []
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_text = soup.get_text()
    email_collection = re.findall(r'[\w\.-]+@[\w\.-]+', page_text)
    email_list.append(email_collection)
    final_df.at[final_df['Website'] == website, 'Email'] = email_list

# Creating a final csv file
final_df.to_csv('./final.csv')
