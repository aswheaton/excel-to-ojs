import os
import numpy as np
import shutil

log = open("log", "w")
f = open('metadata.xml', 'w')
indent_level = 0

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

    return(indent_level * 8 * " ")

def open_tag(tag_name):

    global indent_level
    f.write(indent()+"<"+tag_name+">\n")
    indent_level += 1

def close_tag(tag_name):

    global indent_level
    indent_level -= 1
    f.write(indent()+"</"+tag_name+">\n")

def tag(tag_name, tag_content, **kwargs):

    f.write(indent())
    # Open the tag with any keyword arguments.
    f.write("<"+tag_name)
    for key, value in kwargs:
        f.write(" "+key+"=\""+value)+"\""
    f.write(">")
    # Fill the tag with content.
    f.write(tag_content)
    # Close the tag and move to newline.
    f.write("</"+tag_name+">\n")

"""
Notes:
1. Papers with multiple authors have line ending semicolon, single authors do not!
2. Sec_title column has both "African Elephant and Rhino Group Newsletter" and "Pachyderm".
3. Capitalisation differs for Section column, i.e. "Rhino Notes" and "Rhino notes".
4. Volume contains entries for Vol 42, for which there are no filenames.
5. Number of rows does NOT match number of files in database/articles (extra rows)
   It appears that some files are referenced by multiple rows, for short articles.
6. Not clear wwhat purpose the final column serves.
7. Some filenames in database have capital P, although no such file exists.
"""

for volume in range(1, 42):
    if not os.path.exists("bepress_xml/"+str(volume)+"/1/"):
        os.makedirs("bepress_xml/"+str(volume)+"/1/", mode=0o777)
        log.write("Created directory bepress_xml/{}/1/ with permissions 777.\n".format(volume))

for row in range(1, 10): # dataframe.shape[0]):
    #Get essential info out of the file.
    volume_no = int(dataframe[row][5])
    issue_no = 1

    # Devise a new filename for the file.
    old_filename = str(dataframe[row][10]).lower()
    new_filename = old_filename

    # Copy the file to its new directory, if not already present.
    src = os.path.join("database/articles/", old_filename)
    dst = os.path.join("bepress_xml/", str(volume_no), str(issue_no), new_filename)
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

# Begin writing to the metadata document.
f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
open_tag("documents")
open_tag("document")

for row in range(1, 10):#dataframe.shape[0]):

    title = dataframe[row][1]
    # f.write(indent()+"<titles>\n")
    # indent_level += 1
    # f.write(indent()+"<title>\n")
    # indent_level += 1
    # f.write(indent()+title+"\n")
    # indent_level -= 1
    # f.write(indent()+"</title>\n")
    # indent_level -= 1
    # f.write(indent()+"</titles>\n")
    # indent_level -= 1
    open_tag("titles")
    tag("title", title)
    close_tag("titles")

    volume_no = int(dataframe[row][5])
    pubyear = dataframe[row][3]
    if volume_no % 2 != 0:
        pubdate = str(pubyear)+"-06-30:T00:00:00-07:00" # Why this particular date format?
    elif volume_no % 2 == 0:
        pubdate = str(pubyear)+"-12-31:T00:00:00-07:00" # Why this particular date format?
    # f.write(indent()+"<publication-date>" + pubdate + "</publication-date>" + "\n")
    # f.write(indent()+"<state>published</state>\n")
    tag("publication-date", pubdate)
    tag("state", "published")

    # f.write(indent()+"<authors>\n")
    # indent_level += 1
    open_tag("authors")

    authors = dataframe[row][0]
    author_list = authors.split(";").strip()
    for author in author_list:

        open_tag("author")

        lname = author.split(" ")[0].strip(",")
        tag("lname", lname)
        try:
            fname = author.split(" ")[1].strip()
            tag("fname", fname)
        except IndexError:
            pass
        try:
            mname = author.split(" ")[2].strip()
            tag("mname", mname)
        except IndexError:
            pass

        close_tag("author")

        # f.write(indent()+"<author>\n")
        # indent_level += 1
        # f.write(indent()+"<lname>"+author.split(" ")[0]+"</lname>\n")
        # f.write(indent()+"<fname>"+author.split(" ")[-1]+"</fname>\n")
        # try:
        #     f.write(indent()+"<mname>"+author.split(" ")[1]+"</mname>\n")
        # except IndexError:
        #     pass
        # indent_level -= 1
        # f.write(indent()+"</author>\n")

    # indent_level -= 1
    # f.write(indent()+"</authors>\n")
    close_tag("authors")

    abstract = dataframe[row][8]
    # f.write(indent()+"<abstract>"+abstract+"</abstract>\n")
    tag("abstract", abstract)

    section = dataframe[row][4]
    # f.write(indent()+"<document-type>"+section+"</document-type>\n")
    # f.write(indent()+"<type>article</type>\n")
    tag("document-type", section)
    tag("type", "article")

    page_start, page_end = dataframe[row][6], dataframe[row][7]
    # f.write(indent()+"<fpage>"+page_start+"</fpage>\n")
    # f.write(indent()+"<lpage>"+page_end+"</lpage>\n")
    tag("fpage", page_start)
    tag("lpage", page_end)

# indent_level -= 1
# f.write(indent()+"</document>\n")
# indent_level -=1
# f.write(indent()+"</documents>")
close_tag("document")
close_tag("documents")
