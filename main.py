# So I know how to parse the Criterion website, why would I need this?
# I have txt files for many series (and therefore films) that are no longer
# available in Criterion. Furthermore, the "All Movies" of Criterion
# only lists one country per film. That's a cop out.

#   Overall plan here is to read a file a line at a time. Once
#   I've identified a a title has been found I then start looking
#   for the country (countries) line. I'm hoping to have a list
#   of 'valid' countries to check against to determine of I'm on
#   the correct line. Further, it will validate any new countries
#   that are being introduced.
import os
import re

input_file_directory = 'C:\\Users\\Greg\\Desktop\\Criterion'


def getFilenamesToRead():
    files = [f for f in os.listdir(input_file_directory) if re.match(r'Leaving.*txt', f)]
    return files


def findTitleInLine(line_to_check):
    if re.match(r'^##', line_to_check):
        return None
    return re.findall(r'.*\s\(\d\d\d\d\)', line_to_check)


def extractTitleAndYear(title_with_year):
    open_paren_idx = title_with_year.find("(")
    year = title_with_year[open_paren_idx+1:open_paren_idx + 5]
    title = title_with_year[:open_paren_idx - 1]
    title = title.replace(',', '&CM^')
    return year, title


def loadCountries():
    with open('countries.txt', 'r') as cf:
        countrys = [ln.strip() for ln in cf]
    return countrys

def isThisACountryLine(line, countries_list):
    # Not enuf just to do the simple test, step it up
    # to test all values if you have a match.
    #
    # Due to false positives when actors names had a match
    # for a country, for instance `Frances Lee McCain`.
    if any(country in line for country in countries_list):
        for input_file_country in line.split(','):
            if input_file_country.strip() in countries_list:
                return True
            else:
                return False


def prepareCountriesLine(input_line):
    input_line = input_line.strip()
    return input_line.replace(',', ';')


if __name__ == '__main__':
    files = getFilenamesToRead()
    countries = loadCountries()
    csv_lines = []

    for file in files:
        print("file " + file)
        with open(input_file_directory + "\\" + file, 'r', encoding="utf-8") as f:
            while True:
                titleLine = None
                while not titleLine:
                    line = f.readline()
                    if not line:
                        break
                    titleLine = findTitleInLine(line)
                if not line:
                    break
                if len(titleLine) > 0:
                    year, title = extractTitleAndYear(titleLine[0])
                else:
                    print('Error processing title ' + line + ' in file ' + file)
                line = f.readline()  # skip a line
                if not line:
                    break
                if 'v2' in file:
                    line = f.readline()  # skip a line
                    if not line:
                        break
                line = f.readline()
                if not line:
                    break
                if isThisACountryLine(line, countries):
                    # print(title + ',,' + prepareCountriesLine(line) + ',' + year)
                    csv_lines.append(title + ',,' + prepareCountriesLine(line) + ',' + year)
                else:
                    print("*************Didn't find countries for " + title)

    csv_lines = list(set(csv_lines))

    print()
    print()
    for ln in csv_lines:
        print(ln)
