import pandas as pd

# Wants the information as such:
# State, School, Abbreviation, Type (public/private/community), email, size, website (preferably with LINK hyperlink), notes (if using personal email or issue with contact methods)

# Importing the initial csv file
df = pd.read_csv('./us-colleges-and-universities.csv', encoding='UTF-8', on_bad_lines='skip', delimiter=';')

# Creating the dataframe to convert into a csv file
final_df = pd.DataFrame(columns=['State', 'School', 'Abbreviation', 'Type', 'Email', 'Size', 'Website', 'Notes'])

# Setting shared columns to be the same in the final dataframe
final_df['State'] = df['STATE']
final_df['School'] = df['NAME'].str.title()
final_df['Size'] = df['TOT_ENROLL']

# Creating a column of websites with hyperlink functionality
final_df['Website'] = ['=HYPERLINK("https://'+x+'","LINK")' for x in df['WEBSITE']]

# Creating the type column by mapping the number in the original csv file to a string
school_type = {1: 'Community', 2: 'Private', 3: 'Public'}
final_df['Type'] = df['TYPE'].map(school_type)

# Creating the abbreviation column by splitting the name column and taking the first letter of each word
final_df['Abbreviation'] = [''.join(j[0] for j in x.split()) for x in final_df['School']]

# Creating a final csv file
final_df.to_csv('./final.csv')
