import pandas as pd
import requests
from selenium import webdriver
from tqdm import tqdm
import os

files = os.listdir(os.path.join(os.getcwd(), 'outputs'))

source_files = [file for file in files if 'cleaned' in file]

for source_file in source_files:

    print(f'Pulling references from file {source_file}')

    papers = pd.DataFrame()

    if '.csv' in source_file:
        filepath = os.path.join(os.getcwd(), 'outputs', source_file)
        papers = pd.read_csv(filepath)

    elif '.xlsx' in source_file:
        filepath = os.path.join(os.getcwd(), 'outputs', source_file)
        papers = pd.read_excel(filepath)

    if papers.empty:
        print('No papers found or files not loadable. Aborting...')
        exit()

    search_columns = ['doi','DOI']
    dois = []
    for column in search_columns:
        try:
            dois = papers[column].astype(str).str.strip().tolist()
            print(f'Found dois found for column {column}.')
        except:
            print(f'No dois found for column {column}.')

    if not dois:
        print('No dois found or files not loadable. Aborting...')

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

    if failed_dois:
        print('Outputting failed DOIs')
        failed_dois_df = pd.DataFrame(failed_dois, columns=['DOI'])
        failed_dois_df.to_excel('failed_dois.xlsx', index=False)

    print(f'The following urls will be opened: {urls}')

    web_driver = webdriver.Edge()

    for url in urls:

        web_driver.execute_script("window.open('{url}');".format(url=url))

    print('All DOIs converted to URLs and opened')

    input('Press Enter when finished on the open webpages, they will then close automatically...')














