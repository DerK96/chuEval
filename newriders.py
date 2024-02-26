from bs4 import BeautifulSoup


def count_unique_names(table0_html, table1_html, table2_html):
    soup0 = BeautifulSoup(table0_html, 'html.parser')
    soup1 = BeautifulSoup(table1_html, 'html.parser')
    soup2 = BeautifulSoup(table2_html, 'html.parser')

    table0 = soup0.find('table')
    table1 = soup1.find('table')
    table2 = soup2.find('table')

    if table1 is None or table2 is None or table0 is None:
        print("Error: No table found in one or both files.")
        return

    # Extract names from each table
    names_table0 = set()
    names_table1 = set()
    names_table2 = set()
    for row in table0.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) >= 2:
            name = columns[1].text.strip()
            names_table0.add(name)
    for row in table1.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) >= 2:
            name = columns[1].text.strip()
            names_table1.add(name)

    for row in table2.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) >= 2:
            name = columns[1].text.strip()
            names_table2.add(name)

    print(len(names_table0))
    print(len(names_table1))
    print(len(names_table2))

    # Count unique names appearing only in the second table
    count = 0
    for name in names_table2:
        if name not in names_table1 and name not in names_table0:
            count += 1

    return count


if __name__ == '__main__':
    # Read the HTML content from the first file
    with open('RiderRankingListCombined_19.html', 'r') as file0:
        html_content0 = file0.read()

    with open('RiderRankingListCombined_21_22.html', 'r') as file1:
        html_content1 = file1.read()

    # Read the HTML content from the second file
    with open('RiderRankingListCombined_23.html', 'r') as file2:
        html_content2 = file2.read()

    # Count unique names appearing only in the second table
    unique_names_count = count_unique_names(html_content0, html_content1, html_content2)

    print("Number of persons appearing only in the second table:", unique_names_count)
