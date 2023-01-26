import xml.etree.ElementTree as tree
import pandas as pd

# columns: database, source-app, rec-number, foreign-keys, ref-type, contributors
# titles, pages, volume, number, dates, call-num, urls, research-notes

cols = ["rec-number", "foreign-keys", "ref-type",
        "contributors", "titles", "abstract", "research-notes", "label", "periodical",
        "keywords", "dates", "urls", "work-type"]

rows = []

def getChildren(parent):
    children = []
    if parent != None:
        for child in parent:
            if child is None:
                children.append("")
            else:
                if child.text is not None:
                    children.append(child.text.strip())
                else:
                    children.append("")
    return children

def getTitles(parent):
    titles = []
    if parent != None:
        for title in parent:
            entry = getattr(title.find('style'), 'text', None)
            titles.append(entry)
    return titles

def getKeys(parent):
    keysList = []
    if parent != None:
        for keys in parent:
            entry = getattr(keys.find('style'), 'text', None)
            keysList.append(entry)
    return keysList

def getUrls(parent):
    urlList = []
    if parent != None:
        for urls in parent:
            if urls.tag == 'related-urls':
                for url in urls:
                    entry = getattr(url.find('style'), 'text', None)
                    urlList.append(entry)
    return urlList

def getDates(parent):
    dates = []
    if parent != None:
        for keys in parent:
            if keys.tag == "year":
                dates.append(getattr(keys.find('style'), 'text', None))
            else:
                continue
            if keys.tag == "pub-dates":
                pubDates = keys.find("pub-dates")
                for date in pubDates:
                    dates.append(getattr(date.find('style'), 'text', None))
            else:
                continue
    else:
        return dates
    return dates

def getAuthors(parent):
    authorList = []
    if parent != None:
        for authors in parent:
            for author in authors:
                if author.tag == "author":
                    authorList.append(author.find("style").text)
    return authorList


def convertListToString(list):
    return str(list).replace("[", "").replace("]", "").replace("\'", "")

# getattr(record.find("foreign-keys"), 'text', None)
def main():
    file = tree.parse(input("Provide the filename within the directory to parse: "))
    root = file.getroot()
    count = 0
    for record in root[0]:
        recNumber = getattr(record.find("rec-number"), 'text', None)
        foreignKeys = convertListToString(getChildren(record.find("foreign-keys")))
        refType = getattr(record.find('ref-type'), 'text', None)
        contributors = convertListToString(getAuthors(record.find('contributors')))
        titles = convertListToString(getTitles(record.find('titles')))
        periodical = convertListToString(getChildren(record.find('periodical')))
        abstract = convertListToString(getChildren(record.find('abstract')))
        keywords = convertListToString(getKeys(record.find('keywords')))
        dates = convertListToString(getDates(record.find('dates')))
        urls = convertListToString(getUrls(record.find('urls')))
        workType = convertListToString(getChildren(record.find('work-type')))
        researchNotes = convertListToString(getChildren(record.find('research-notes')))
        label = convertListToString(getChildren(record.find('label')))

        entry = {'rec-number': recNumber,
                 'foreign-keys': foreignKeys,
                 'ref-type': refType,
                 'abstract': abstract,
                 'contributors': contributors,
                 'titles': titles,
                 'periodical': periodical,
                 'keywords': keywords,
                 'dates': dates,
                 'urls': urls,
                 'work-type': workType,
                 'research-notes': researchNotes,
                 'label': label}

        rows.append(entry)

        count += 1

    df = pd.DataFrame(rows, columns=cols)

    df.to_csv("output.csv")

if __name__ == '__main__':
    main()