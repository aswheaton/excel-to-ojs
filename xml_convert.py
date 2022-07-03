import os
import numpy as np
import shutil

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

def view_headers(dataframe):

    print(dataframe[0,:])
    log.write("Viewing dataframe headers, they are {}.\n".format(dataframe[0,:]))

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
    for key, value in kwargs:
        f.write(" "+key+"=\""+value)+"\""
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
TODO: Volume contains entries for Vol 42, for which there are no filenames.
TODO: Number of rows does NOT match number of files in database/articles (extra rows)
TODO: It appears that some files are referenced by multiple rows, for short articles. FIXED!
TODO: Not clear wwhat purpose the final column serves. FIXED!
TODO: Some filenames in database have capital P, although no such file exists. FIXED, kinda!
TODO: Check logic of directory structure creation for missing file in row 1.
"""

for row in range(1, 10): # dataframe.shape[0]):
    #Get essential info out of the file.
    volume_no = int(dataframe[row][5])
    issue_no = 1

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

    if not os.path.exists("bepress_xml/"+str(volume_no)+"/1/"+str(article_no)):
        os.makedirs("bepress_xml/"+str(volume_no)+"/1/"+str(article_no), mode=0o777)
        log.write("Created directory bepress_xml/{}/{}/{} with permissions 777.\n".format(volume_no, issue_no, article_no))

    # Copy the file to its new directory, if not already present.
    src = os.path.join("database/articles/", old_filename.lower()) # Actual filenames do not contain captial letters.
    dst = os.path.join("bepress_xml/", str(volume_no), str(issue_no), str(article_no), new_filename)
    log.write("Copying file {} to {}.\n".format(src, dst))

    if not os.path.exists(dst):
        try:
            shutil.copy2(src, dst)
        except FileNotFoundError:
            src = input("No file found at {}, input source or skip: ".format(src))
            if src != "skip":
                shutil.copy2(src, dst)
            else:
                pass

    # Now create the requisite metadata file for the article.
    xml_file_path = "bepress_xml/{}/{}/{}/metadata.xml".format(volume_no, issue_no, article_no)
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

    # volume_no = int(dataframe[row][5])
    # pubyear = dataframe[row][3]
    # if volume_no % 2 != 0:
    #     pubdate = str(pubyear)+"-06-30:T00:00:00-07:00" # Why this particular date format?
    # elif volume_no % 2 == 0:
    #     pubdate = str(pubyear)+"-12-31:T00:00:00-07:00" # Why this particular date format?

    pubdate = pubdates[volume_no]
    tag("publication-date", pubdate)
    tag("state", "published")

    open_tag("authors")
    authors = dataframe[row][0]
    author_list = authors.split(";")

    for author in author_list:

        open_tag("author")

        names = author.strip().split(" ")
        lname = names[0].strip(",")

        if lname in author_emails.keys():
            author_email = author_emails[lname]
        else:
            author_email = "example@example.com"

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
            tag("lname", lname)
        if fname != None:
            tag("fname", fname)
        if mname != None:
            tag("mname", mname)

        # print(author.strip())
        # print(lname+"!")
        # try:
        #     print(fname+"!")
        # except TypeError:
        #     pass
        # try:
        #     print(mname+"!")
        # except TypeError:
        #     pass

        close_tag("author")
    close_tag("authors")


    abstract = dataframe[row][8]
    tag("abstract", abstract)

    section = dataframe[row][4]
    tag("document-type", section)
    tag("type", "article")

    page_start, page_end = dataframe[row][6], dataframe[row][7]
    tag("fpage", page_start)
    tag("lpage", page_end)

    close_tag("document")
    close_tag("documents")
