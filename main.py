import pandas as pd
from usp.tree import sitemap_tree_for_homepage

# Wants the information as such:
# State, School, Abbreviation, Type (public/private/community), SGA email, size, SGA website (preferably with LINK hyperlink), notes (if using personal email or issue with contact methods)

# Importing the initial csv file
df = pd.read_csv('./us-colleges-and-universities.csv', encoding='UTF-8', on_bad_lines='skip', delimiter=';')

# Creating the dataframe to convert into a csv file
final_df = pd.DataFrame(columns=['State', 'School', 'Abbreviation', 'Type', 'Email', 'Size', 'Website', 'Address', 'Notes'])

# Setting shared columns to be the same in the final dataframe
final_df['State'] = df['STATE']
final_df['School'] = df['NAME'].str.title()
final_df['Size'] = df['TOT_ENROLL'].replace(-999, 'N/A')

# Creating a column of websites with hyperlink functionality
# final_df['Website'] = ['=HYPERLINK("https://www.'+x.replace('https://', '').replace('www.','')+'","LINK")' for x in df['WEBSITE']]
# The website needs to be the SGA website, not the school's website

# Creating the type column by mapping the number in the original csv file to a string
school_type = {1: 'Community', 2: 'Private', 3: 'Public'}
final_df['Type'] = df['TYPE'].map(school_type)

# Creating the abbreviation column by splitting the name column and taking the first letter of each word
articles = ['the', 'of', 'and', 'at', 'a', 'an', '&']
final_df['Abbreviation'] = [''.join(j[0] for j in x.split() if j.lower() not in articles) for x in final_df['School']]

# Creating the address column
final_df['Address'] = df['ADDRESS'].str.title() + ', ' + df['CITY'].str.title() + ', ' + df['STATE'].str.upper() + ' ' + df['ZIP'].astype(str)

# Creating a final csv file
final_df.to_csv('./final.csv')
