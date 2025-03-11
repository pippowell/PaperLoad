import pandas as pd
import requests
from selenium import webdriver
from tqdm import tqdm

source_file = input('Please copy the path to the csv or Excel file containing the references. \n File Address: ')

source_file = source_file.replace("\\","/")[1:-1]

print(f'Pulling references from file {source_file}')

if '.csv' in source_file:
    papers = pd.read_csv(source_file)

elif '.xlsx' in source_file:
    papers = pd.read_excel(source_file)

try:
    dois = papers['doi'].astype(str).str.strip().tolist()
except:
    dois = papers['DOI'].astype(str).str.strip().tolist()

urls = []
failed_dois = []

attempt_limit = 5

cleaned_dois = [item for item in dois if item != 'nan']

print(f'The following DOIS will be converted to URLs: {cleaned_dois}')

for doi in tqdm(cleaned_dois):
    url = f'https://doi.org/{doi}'

    attempts = 1
    success = False

    while attempts <= attempt_limit and success == False:
        try:
            response = requests.get(url,timeout=10)
            url = response.url
            urls.append(url)
            success = True

        except:
            print(f'URL pull with doi {doi} failed. Will attempt {5-attempts} more times')
            attempts += 1

    if attempts == 6:
        print(f'Max attempts reached. Failed to pull URL for DOI {doi}. Making note.')
        failed_dois.append(doi)

print('Outputting failed DOIs')
failed_dois_df = pd.DataFrame(failed_dois, columns=['DOI'])
failed_dois_df.to_excel('failed_dois.xlsx', index=False)

print(f'The following urls will be opened: {urls}')

web_driver = webdriver.Edge()

for url in urls:

    web_driver.execute_script("window.open('{url}');".format(url=url))

print('All DOIs converted to URLs and opened')












