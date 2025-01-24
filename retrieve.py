import json
import os
import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.justice.gov/usao-dc/capitol-breach-cases"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the case information
table = soup.find('table')

# Iterate over the rows of the table
case_info = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    cells = row.find_all('td')
    if len(cells) > 1:
        name = cells[1].get_text(strip=True)
        link = cells[1].find('a')['href'] if cells[1].find('a') else 'No link'
        # print(f"Name: {name}, Link: {link}")
    case_info.append((name, link))

print(case_info)
# Iterate over the pages
for page in range(1, 42):
    # Update the URL with the current page number
    paginated_url = f"https://www.justice.gov/usao-dc/capitol-breach-cases?page={page}"
    print(f"Fetching page {page}...")
    
    # Send a GET request to the paginated URL
    response = requests.get(paginated_url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the case information
    table = soup.find('table')
    
    # Iterate over the rows of the table
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        if len(cells) > 1:
            name = cells[1].get_text(strip=True)
            link = cells[1].find('a')['href'] if cells[1].find('a') else 'No link'
            case_info.append((name, link))

# Print the collected case information
# print(case_info)
# Print the total number of cases collected
print(len(case_info))

# Create the directory if it doesn't exist
if not os.path.exists('casefiles'):
    os.makedirs('casefiles')

for each in case_info:
    full_url = "https://www.justice.gov" + each[1]
    print(full_url)

    # Send a GET request to the full URL
    doc_response = requests.get(full_url)

    # Parse the HTML content of the page
    doc_soup = BeautifulSoup(doc_response.content, 'html.parser')

    # Find the section containing the associated documents
    associated_docs_section = doc_soup.find('div', class_='field__item downloadable downloadable__attachment')

    if associated_docs_section:
        # Find all links to the associated documents
        doc_links = associated_docs_section.find_all('a')
        for doc_link in doc_links:
            doc_url = "https://www.justice.gov" + doc_link['href']
            doc_name = doc_link.get_text(strip=True).replace('/', '_') + '.pdf'
            
            
            # Save the document to the casefiles directory
            filename = (each[0]+'-'+doc_name).replace(" ", "_").replace('"','')
            if not os.path.exists(os.path.join('casefiles', filename)):
                # Download the document
                doc_content = requests.get(doc_url).content
                print(f"Downloading {doc_name}...")
                with open(os.path.join('casefiles', filename), 'wb') as doc_file:
                    doc_file.write(doc_content)
            else:
                print(f"{filename} already exists. Skipping download.")


# Save the case information to a json file

with open('case_info.json', 'w') as f:
   json.dump(case_info, f)

# # Save the case information to a csv file
# import csv
# with open('case_info.csv', 'w', newline='') as f:
#   writer = csv.writer(f)
# writer.writerow(['Name', 'Link'])
# for case in case_info:
#   writer.writerow(case)
# # Save the case information to a txt file
# with open('case_info.txt', 'w') as f:
#  for case in case_info:
#   f.write(f"{case[0]}: {case[1]}\n")
# # Save the case information to a pickle file
# import pickle
# with open('case_info.pkl', 'wb') as f:
# pickle.dump(case_info, f)
# # Save the case information to a sqlite database
# import sqlite3
# conn = sqlite3.connect('case_info.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE IF NOT EXISTS cases
# (name TEXT, link TEXT)''')
# for case in case_info:
# c.execute("INSERT INTO cases VALUES (?, ?)", case)
# conn.commit()
# conn.close()
#   
