import os
import numpy as np
import shutil

journal_name = "Pachyderm"

pubdates = {
    1  : "1983-04-30:T12:00:00+03:00", # April 1983.
    2  : "1983-11-30:T12:00:00+03:00", # November 1983.
    3  : "1984-06-30:T12:00:00+03:00", # June 1984.
    4  : "1984-12-30:T12:00:00+03:00", # December 1984.
    5  : "1985-07-30:T12:00:00+03:00", # July 1985.
    6  : "1986-02-28:T12:00:00+03:00", # February 1986.
    7  : "1986-12-30:T12:00:00+03:00", # December 1986
    8  : "1987-04-30:T12:00:00+03:00", # April 1987.
    9  : "1987-12-30:T12:00:00+03:00", # December 1987.
    10 : "1988-01-30:T12:00:00+03:00", # January 1988. Short publishing interval.
    11 : "1989-06-30:T12:00:00+03:00", # No exact date given.
    12 : "1989-12-30:T12:00:00+03:00", # No exact date given.
    13 : "1990-12-30:T12:00:00+03:00", # No exact date given.
    14 : "1991-12-30:T12:00:00+03:00", # No exact date given.
    15 : "1992-12-30:T12:00:00+03:00", # No exact date given.
    16 : "1993-06-30:T12:00:00+03:00", # No exact date given.
    17 : "1993-12-30:T12:00:00+03:00", # No exact date given.
    18 : "1994-12-30:T12:00:00+03:00", # No exact date given.
    19 : "1995-06-30:T12:00:00+03:00", # No exact date given.
    20 : "1995-12-30:T12:00:00+03:00", # No exact date given.
    21 : "1996-06-30:T12:00:00+03:00", # No exact date given.
    22 : "1996-12-30:T12:00:00+03:00", # No exact date given.
    23 : "1997-06-30:T12:00:00+03:00", # No exact date given.
    24 : "1997-12-30:T12:00:00+03:00", # JAN-DEC 1997. Conlficts with previous date range. Article footers say JUL-DEC 1997.
    25 : "1998-07-15:T12:00:00+03:00", # JAN-JUL 1998.
    26 : "1998-12-30:T12:00:00+03:00", # JUL-DEC 1998.
    27 : "1999-12-30:T12:00:00+03:00", # JAN-DEC 1999.
    28 : "2000-06-30:T12:00:00+03:00", # JAN-JUN 2000.
    29 : "2000-12-30:T12:00:00+03:00", # JUL-DEC 2000.
    30 : "2001-06-30:T12:00:00+03:00", # JAN-JUN 2001.
    31 : "2001-12-30:T12:00:00+03:00", # JUL-DEC 2001.
    32 : "2002-06-30:T12:00:00+03:00", # JAN-JUN 2002.
    33 : "2002-12-30:T12:00:00+03:00", # JUL-DEC 2002.
    34 : "2003-06-30:T12:00:00+03:00", # JAN-JUN 2003.
    35 : "2003-12-30:T12:00:00+03:00", # JUL-DEC 2003.
    36 : "2004-06-30:T12:00:00+03:00", # JAN-JUN 2004.
    37 : "2004-12-30:T12:00:00+03:00", # JUL-DEC 2004.
    38 : "2005-06-30:T12:00:00+03:00", # JAN-JUN 2005.
    39 : "2005-12-30:T12:00:00+03:00", # JUL-DEC 2005.
    40 : "2006-06-30:T12:00:00+03:00", # JAN-JUN 2006.
    41 : "2006-12-30:T12:00:00+03:00", # JUL-DEC 2006.
    }

author_emails = {
    "Ghosh"         : "Omitted from public repository.",
    "Rookmaaker"    : "Omitted from public repository.",
    "Nishihara"     : "Omitted from public repository.",
    "Hillman"       : "Omitted from public repository.",
    "Hillman-Smith" : "Omitted from public repository.",
    "Stiles"        : "Omitted from public repository.",
    "Vigne"         : "Omitted from public repository.",
    "Schulte"       : "Omitted from public repository.",
    "Lindsay"       : "Omitted from public repository.",
    "Hoare"         : "Omitted from public repository.",
    "Potter"        : "Omitted from public repository."
    }

log = open("log", "w")

dataframe = np.loadtxt("database/Pachy.csv",dtype=str,delimiter="	")
log.write("Successfully loaded CSV file into dataframe.\n")

aggregate_authors = []

def view_headers(dataframe):

    print(dataframe[0,:])
    # log.write("Viewing dataframe headers, they are {}.\n".format(dataframe[0,:]))

def view_column(dataframe, column_name):
    # Get index associated with the column name:
    col = np.where(dataframe[0,:]==column_name)
    for row in range(1, dataframe.shape[0]):
        print(row, dataframe[row][col])

def indent():

    return(indent_level * "	")

def open_tag(tag_name):

    global indent_level
    xml_file.write(indent()+"<"+tag_name+">\n")
    indent_level += 1

def close_tag(tag_name):

    global indent_level
    indent_level -= 1
    xml_file.write(indent()+"</"+tag_name+">\n")

def tag(tag_name, tag_content, **kwargs):

    xml_file.write(indent())
    # Open the tag with any keyword arguments.
    xml_file.write("<"+tag_name)
    for key, value in kwargs.items():
        xml_file.write(" " + key + "=\"" + value + "\"")
    xml_file.write(">")
    # Fill the tag with content.
    xml_file.write(tag_content)
    # Close the tag and move to newline.
    xml_file.write("</"+tag_name+">\n")

"""
Notes:
TODO: Papers with multiple authors have line ending semicolon, single authors do not! FIXED!
TODO: Sec_title column has both "African Elephant and Rhino Group Newsletter" and "Pachyderm".
TODO: Capitalisation differs for Section column, i.e. "Rhino Notes" and "Rhino notes".
TODO: Volume contains entries for Vol 42, for which there are no filenames. FIXED!
TODO: Number of rows does NOT match number of files in database/articles (extra rows) FIXED!
TODO: It appears that some files are referenced by multiple rows, for short articles. FIXED!
TODO: Not clear what purpose the final column serves. FIXED!
TODO: Some filenames in database have capital P, although no such file exists. FIXED, kinda!
TODO: Check logic of directory structure creation for missing file in row 1. WORKS!
TODO: Add section names (either <type> or <document-type>) and <galley> tags.
"""

for row in range(1, dataframe.shape[0]):
    #Get essential info out of the file.
    volume_no = int(dataframe[row][5])
    issue_no = 1

    if volume_no == 42:
        log.write("Volume number exceeds available galleys! Stopping conversion.\n")
        break

    # If this is the first article in the first issue, start an article counter at 1.
    if row == 1:
        article_no = 1
    # If this is the beginning of a new issue, reset the article counter.
    elif volume_no != int(dataframe[row-1][5]):
        article_no = 1
    # If the article is in the same issue as the previous, increment the article counter.
    elif volume_no == int(dataframe[row-1][5]):
        article_no += 1

    # Devise a new filename for the file.
    old_filename = str(dataframe[row][10])
    new_filename = old_filename.lower()

    article_path = os.path.join("bepress_xml", journal_name, str(volume_no), str(issue_no), str(article_no))
    if not os.path.exists(article_path):
        os.makedirs(article_path, mode=0o777)
        log.write("Created directory {} with permissions 777.\n".format(article_path))

    # Copy the file to its new directory, if not already present.
    src = os.path.join("database/articles/", old_filename.lower()) # Actual filenames do not contain captial letters.
    dst = os.path.join(article_path, new_filename)

    if not os.path.exists(dst):
        try:
            shutil.copy2(src, dst)
            log.write("Copied file {} to {}.\n".format(src, dst))
        except FileNotFoundError:
            log.write("Error in row {}. Could not find a file at {}, writing metadata anyway.\n".format(row+1, src))

    # Now create the requisite metadata file for the article.
    xml_file_path = os.path.join(article_path, "metadata.xml")
    xml_file = open(xml_file_path, "w")
    indent_level = 0

    # Begin writing to the metadata document.
    xml_file.write("<?xml version='1.0' encoding='utf-8' ?>\n")
    open_tag("documents")
    open_tag("document")

    title = dataframe[row][1]
    open_tag("titles")
    tag("title", title)
    close_tag("titles")

    pubdate = pubdates[volume_no]
    tag("publication-date", pubdate)
    tag("state", "published")

    open_tag("authors")
    authors = dataframe[row][0]
    author_list = authors.split(";")

    for author in author_list:

        aggregate_authors.append(author.strip())

        open_tag("author")

        names = author.strip().split(" ")
        lname = names[0].strip(",")

        if lname in author_emails.keys():
            author_email = author_emails[lname]
        else:
            author_email = "AfESG@iucn.org"

        try:
            fname = names[1]
        except IndexError:
            fname = None
        try:
            mname = names[2]
            for i in range(3, len(names)):
                mname += " " + names[i]
        except IndexError:
            mname = None

        tag("email", author_email)
        if lname != None:
            tag("lname", lname, locale="en_US")
        if fname != None:
            tag("fname", fname, locale="en_US")
        if mname != None:
            tag("mname", mname, locale="en_US")

        close_tag("author")
    close_tag("authors")


    abstract = dataframe[row][8]
    tag("abstract", abstract)

    open_tag("galleys")
    tag("galley", new_filename, locale="en_US")
    close_tag("galleys")

    section = dataframe[row][4]
    tag("document-type", section)
    tag("type", "article")

    page_start, page_end = dataframe[row][6], dataframe[row][7]
    tag("fpage", page_start)
    tag("lpage", page_end)

    close_tag("document")
    close_tag("documents")

    xml_file.close()

for volume_no in range(1,42):

    issue_no = 1

    if volume_no < 10:
        old_cover_filename = "cv-pachy0" + str(volume_no) + ".jpg"
    else:
        old_cover_filename = "cv-pachy" + str(volume_no) + ".jpg"

    src = os.path.join("database/covers/", old_cover_filename)
    dst = os.path.join("bepress_xml/", journal_name, str(volume_no), str(issue_no), "cover.jpg")
    shutil.copy2(src, dst)
    log.write("Copied {} to {}.\n".format(src, dst))

publication_threshold = 3

unique_authors = np.unique(aggregate_authors).tolist()
unique_authors.remove("")
unique_author_contributions = []
reduced_unique_authors = []

for i in range(len(unique_authors)):
    unique_author_contributions.append(aggregate_authors.count(unique_authors[i]))

for i in range(len(unique_authors)):
    if unique_author_contributions[i] >= publication_threshold:
        reduced_unique_authors.append(unique_authors[i])

# for i in range(len(reduced_unique_authors)):
#     log.write("Author {} is a contributor on {} articles.\n".format(reduced_unique_authors[i], aggregate_authors.count(reduced_unique_authors[i])))

contributions = 0
for row in range(1, dataframe.shape[0]):
    for author in reduced_unique_authors:
        if author in dataframe[row,0]:
            # log.write("Found {} in {}.\n".format(author, dataframe[row,0]))
            contributions +=1
            break

log.write("Found {} unique authors who have published {} or more papers.\n".format(len(reduced_unique_authors), publication_threshold))
log.write("The authors are:\n")
for author in reduced_unique_authors:
    log.write("{}; \n".format(author))
log.write("{}% of contributions are from these {} individuals.\n".format(contributions/row*100, len(reduced_unique_authors)))

"""
Found 160 unique authors who have published 2 or more papers.
79.50% of contributions are from these 160 individuals.
Found 86 unique authors who have published 3 or more papers.
68.27% of contributions are from these 86 individuals.
Found 52 unique authors who have published 4 or more papers.
59.26% of contributions are from these 52 individuals.
Found 38 unique authors who have published 5 or more papers.
53.39% of contributions are from these 38 individuals.
Found 27 unique authors who have published 6 or more papers.
47.91% of contributions are from these 27 individuals.
Found 19 unique authors who have published 7 or more papers.
42.55% of contributions are from these 19 individuals.
Found 19 unique authors who have published 8 or more papers.
42.55% of contributions are from these 19 individuals.
Found 17 unique authors who have published 9 or more papers.
40.73% of contributions are from these 17 individuals.
Found 17 unique authors who have published 10 or more papers.
40.73% of contributions are from these 17 individuals.

2+ papers -> 160 unique authors comprising 79.50% of all articles.
3+ papers -> 86 unique authors comprising 68.27% of all articles.
4+ papers -> 52 unique authors comprising 59.26% of all articles.
5+ papers -> 38 unique authors comprising 53.39% of all articles.
6+ papers -> 27 unique authors comprising 47.91% of all articles.
7+ papers -> 19 unique authors comprising 42.55% of all articles.
8+ papers -> 19 unique authors comprising 42.55% of all articles.
9+ papers -> 17 unique authors comprising 40.73% of all articles.
10+ papers -> 17 unique authors comprising 40.73% of all articles.
"""

log.close()
