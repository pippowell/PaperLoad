import pandas as pd
import os
import datetime

def multi_line(text, max_length):

    words = text.split()

    lines = []

    current_line = ''

    for word in words:

        if len(current_line) + len(word) >= max_length:
            lines.append(current_line)
            current_line = word
        else:
            current_line = current_line + " " + word

    lines.append(current_line)

    return '\n'.join(lines)


# locates entries that are unique across the files while leaving duplicate entries within the files
def find_unique_entries(files, combined_file, duplicates_file, frequent_duplicates_file, column, keep_dups):

    # load the files
    raw_csvs = {}

    for i,file in enumerate(files):
        filepath = os.path.join(os.getcwd(), 'raw_files',file)
        df = pd.read_csv(filepath)
        df['source'] = f'file{i}'
        raw_csvs[i] = df

    dup_across = []

    # combine their dataframes
    combined = pd.concat(raw_csvs.values(), ignore_index=True)

    final_columns = ['source','date','title','doi','authors','journal','short_journal','volume','year','publisher','issue','page','abstract']

    combined = combined[final_columns]

    print(f'Total number of papers across all provided files before duplication removal: {len(combined)}')

    if keep_dups:

        # locate duplicates across the files and save them
        find_dups = combined.duplicated(subset=[column],keep=False)

        dups = combined[find_dups]

        dups.to_excel(duplicates_file, index=False)

        print(f'Combined file with all duplicates created at {combined_file}')

        dup_counts = dups[column].value_counts()

        dups_three_plus = dup_counts[dup_counts >= 3].index

        final_dups = dups[dups[column].isin(dups_three_plus)]

        final_dups_multiline = final_dups.map(lambda x: multi_line(x, 300) if isinstance(x, str) else x)

        final_dups_multiline.to_excel(frequent_duplicates_file,index=False)

        print(f'Combined file with frequent duplicates created at {combined_file}')

    # remove duplicates based on the desired field
    unique = combined.drop_duplicates(subset=[column], keep='first')

    unique_multiline = unique.map(lambda x: multi_line(x, 150) if isinstance(x, str) else x)

    # save the unique entries
    unique_multiline.to_excel(combined_file, index=False)

    print(f'Total number of papers across all provided files after duplication removal: {len(unique_multiline)}')

    print(f'Final cleaned file with only unique papers created at {combined_file}')

    return dup_across

files = os.listdir(os.path.join(os.getcwd(), 'raw_files'))
work_dir = os.getcwd()
timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
combined_file = os.path.join(work_dir,'outputs',f'{timestamp}_cleaned.xlsx')
duplicates_file = os.path.join(work_dir,'outputs',f'{timestamp}_all_duplicates.xlsx')
frequent_duplicates_file = os.path.join(work_dir,'outputs',f'{timestamp}_frequent_duplicates.xlsx')
column = 'doi'
keep_dups = True

find_unique_entries(files, combined_file, duplicates_file, frequent_duplicates_file, column, keep_dups)








