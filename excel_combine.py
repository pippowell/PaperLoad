import pandas as pd

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
def find_unique_entries(file1, file2, combined_file, duplicates_file, column, keep_dups):

    # load the files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    dup_across = []

    # track source file
    df1['source'] = 'file1'
    df2['source'] = 'file2'

    # combine their dataframes
    combined = pd.concat([df1, df2])

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


file1 = "C:/Users/powel/Documents/how-can-I-detect-water-stress-in-vegetables-using-cameras-and-sensors_2025-02-13091439_export.xlsx"
file2 = "C:/Users/powel/Documents/how-can-I-detect-water-stress-in-vegetables-using-cameras-and-sensors_2025-02-13093029_export.xlsx"
combined_file = 'C:/Users/powel/Documents/water_stress_detection_vegetables_papers.xlsx'
duplicates_file = 'C:/Users/powel/Documents/duplicate_papers.xlsx'
column = 'title'
keep_dups = True

find_unique_entries(file1, file2, combined_file, duplicates_file, column, keep_dups)








