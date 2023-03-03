import os

# list of cobiss id already present from the previous file, as csv
with open('cobiss.csv') as f:
    cobList = f.read()
    f.close()
cobList = cobList.splitlines()
cobList.pop(0)

# list of all datas from xml
data_list = []

# open all files from folder, open in loop all .xml, saves all to data_list
Path = "."
filelist = os.listdir(Path)
for files in filelist:
    if files.endswith(".xml"):
        with open(files) as f:
            data = f.read().strip("\n")
            f.close()
            # clean front of xml file
            data = data.split("<BiblioList>")
            data.pop(0)
            data_list.extend(data)

# generate dictionary with cobiss as key, containing category and rest of the article
dictionary = {}
for categories in data_list:
    category = categories.split("</Title>", 1).pop(0)
    category = category.split("<Title>").pop(1)
    articles = categories.split('<BiblioEntry bno="')
    articles.pop(0)
    for article in articles:
        cobiss = article.split('<COBISS co="SI" id="').pop(1)
        cobiss = cobiss.split('">').pop(0)
        if cobiss not in dictionary.keys():
            dictionary.update({cobiss: (category, article)})

# generate researchers info
with open("ResearchersAffAndCountry.csv") as f:
    # I got the .csv by copying all the existing data, and deleting the affiliation row, saving me time with IR author. Also added all IR employed people.
    dataInfoonresearchers = f.readlines()
    f.close()

# researcher data dictionary, with names as keys
reseatcherDataInfo = {}
for lines in dataInfoonresearchers:
    lines = lines.strip("\n").split(",")
    if lines[0] not in reseatcherDataInfo.keys():
        reseatcherDataInfo.update({lines[0]: (lines[1], lines[2], lines[3], lines[4])})

# researchers information like nationality, affiliation
def researcherinfo(name):
    for keys in reseatcherDataInfo.keys():
        if name == keys:
            ir_aff1 = reseatcherDataInfo[name][0]
            #ir_aff2 = reseatcherDataInfo[name][1]
            conuntry1 = reseatcherDataInfo[name][2]
            conuntry2 = reseatcherDataInfo[name][3]
            # Innorenew affiliation is blank, as it is paper dependent.
            # In case in the future if there are people with known IR affiliation but not employed, like students,
            # you could add an exception and delete all the affiliation from other people except them.
            string = ir_aff1 + "\t" + """ir_aff2 +"""  "\t" + conuntry1 + "\t" + conuntry2
            return string
    return "No \t\t\t"  # if they are not in the list of researchers, they can not be employed

# function to write data to tbv file
def writeline(cobiskey):
    # cobiss id
    cobisToFile = cobiskey

    # article cathegory
    articleCategory = dictionary[cobiskey][0]

    # all the rest needed for the extraction
    restOfFile = dictionary[cobiskey][1]

    # title
    dirty = restOfFile
    title = dirty.split('<Title>', 1).pop(1)
    title = title.split('</Title>').pop(0)
    title = title.replace("\n", "").replace("\r\n", "")

    # year
    try:
        dirty = restOfFile
        year = dirty.split('<PubDate>').pop(1)
        year = year.split('</PubDate>').pop(0)
        year = int(''.join(filter(str.isdigit, year)))

    except:
        year = "year not present"  # prefer this over blank, as it is more easily searchable

    # citations
    try:
        dirty = restOfFile
        citations = dirty.split('CI="').pop(1)
        citations = citations.split('"').pop(0)

    except:
        citations = "cit not present"  # prefer this over blank, as it is more easely searchable

    # authors
    list_of_authors = []
    dirty = restOfFile
    authors = dirty.split('<AuthorGroup').pop(1)
    authors = authors.split('</AuthorGroup>').pop(0)
    authors = authors.split("</Author>")
    authors.pop(len(authors) - 1)
    for author in authors:
        author_inloop = author
        surname = author_inloop.split("</SurName>").pop(0)
        surname = surname.split("<SurName>").pop(1)
        surname = surname.upper()
        name = author_inloop.split("</FirstName>").pop(0)
        name = name.split("<FirstName>").pop(1)
        list_of_authors.append(surname + " " + name)

    # title of journal
    dirty = restOfFile
    try:
        journal_title = dirty.split('<BiblioSet relation="journal">').pop(1)
        journal_title = journal_title.split('</Title>').pop(0)
        journal_title = journal_title.rsplit('<Title>').pop(1)
        journal_title = journal_title.replace("\n", "").replace("\r\n", "")
    except:
        journal_title = "journal not present"

    # write to .tsv
    f = open("output.tsv", "a")
    for people in list_of_authors:
        info = researcherinfo(people)
        string_toFile = "\t" + cobisToFile + "\t" + title + "\t" + people + "\t" + info + "\t" + articleCategory + "\t" + str(
            year) + "\t" + journal_title + "\t\t\t" + citations + "\n"
        f.writelines(string_toFile)
    f.close()

# check if cobiss is already present in the Excel
a = dictionary.keys()
b = cobList
for element in a:
    if element not in b:
        # call writeline function
        writeline(element)
