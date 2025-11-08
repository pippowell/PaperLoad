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
def find_unique_entries(files, combined_file, duplicates_file, column, keep_dups):

    # load the files
    raw_csvs = {}

    for i,file in enumerate(files):
        filepath = os.path.join(os.getcwd(), 'raw_files',file)
        df = pd.read_csv(filepath)
        df['source'] = f'file{i}'
        raw_csvs[i] = df

    dup_across = []

    print(raw_csvs[1])

    # combine their dataframes
    combined = pd.concat(raw_csvs.values(), ignore_index=True)

    if keep_dups:

        # locate duplicates across the files and save them
        find_dups = combined.duplicated(subset=[column],keep=False)

        dups = combined[find_dups]

        dups.to_excel('dups.xlsx', index=False)

        dup_counts = dups[column].value_counts()

        dups_three_plus = dup_counts[dup_counts >= 3].index

        final_dups = dups[dups[column].isin(dups_three_plus)]

        final_dups_multiline = final_dups.applymap(lambda x: multi_line(x, 300) if isinstance(x, str) else x)

        final_dups_multiline.to_excel(duplicates_file,index=False)

    # remove duplicates based on the desired field
    unique = combined.drop_duplicates(subset=[column], keep='first')

    unique_multiline = unique.applymap(lambda x: multi_line(x, 150) if isinstance(x, str) else x)

    # save the unique entries
    unique_multiline.to_excel(combined_file, index=False)

    print(f'Combined file with unique entries only created as {combined_file}')

    return dup_across

files = os.listdir(os.path.join(os.getcwd(), 'raw_files'))
work_dir = os.getcwd()
timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
combined_file = os.path.join(work_dir,'outputs',f'{timestamp}_combined_papers.xlsx')
duplicates_file = os.path.join(work_dir,'outputs',f'{timestamp}_duplicates.xlsx')
column = 'title'
keep_dups = True

find_unique_entries(files, combined_file, duplicates_file, column, keep_dups)








