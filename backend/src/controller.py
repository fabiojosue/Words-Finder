from distutils import text_file
import PyPDF2
import subprocess
from impala.dbapi import connect

####################################
# POST '/book'
####################################

txtFile = 'currentBook.txt'

# Function to convert a .pdf file into .txt

def pdfToTxt(file):
    specialCharacters = [
                        " ",",",".",":",";",
                        "(",")","!","¡","¿",
                        "?","_","-","'","–",
                        "\"","\n","\t","•","”","—"
                        ]

    pdfReader = PyPDF2.PdfFileReader(open(file,'rb'))
    numPages = pdfReader.numPages

    with open('./staticFiles/' + txtFile, 'w') as f:
        for i in range(numPages):
            currentPage = pdfReader.getPage(i)
            text = currentPage.extractText()
            for j in range(len(text)):
                if text[j] not in specialCharacters:
                    f.write(text[j].lower())
                else:
                    if text[j-1] not in specialCharacters:
                        f.write("\n")

# Function to run any Linux command in cmd
# Implemented by Morteza Mashayekhi
# Function vision for Hadoop commands
# @ https://stackoverflow.com/questions/26606128/how-to-save-a-file-in-hadoop-with-python

def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err 

# Function that takes a string of words separated by " " or "," and returns a list with each word separated

def wordsToList(words):
    delimiters = [" ",","]
    wordList = []
    currentWord = ""

    for i in range(len(words)):
        if words[i] not in delimiters:
            currentWord+=words[i]
        else:
            wordList.append(currentWord)
            currentWord = ""

    wordList.append(currentWord)
    return wordList


# Function to save the hdfs file data into impala table (1st cursor)
# 2nd and 3rd cursor gets the data we looking for

def loadIntoImpala(words):
    wordList = wordsToList(words)
    wordDict = {"words":{}}

    conn = connect(host = "172.17.0.2", port = 21050)
    cursor = conn.cursor()

    cursor.execute("load data inpath 'hdfs://172.17.0.01:9000/tmp/csv/" + txtFile + "'" + " overwrite into table bd2.book ;") 

    for i in range(len(wordList)):
        cursor.execute("select count(*) from bd2.book where word='"+wordList[i]+"';")
        wordDict["words"].update({wordList[i]:cursor.next()[0]})

    cursor.execute("select count(*) from bd2.book;")
    totalWords = {"totalWords":cursor.next()[0]} 

    cursor.close()
    conn.close()

    return wordDict | totalWords

def interactBook(words,file):
    pdfToTxt(file)
    run_cmd(['hdfs', 'dfs', '-put', '/home/fabio/bd2-impala/Words-Finder/backend/src/staticFiles/' + txtFile, '/tmp/csv'])
    return loadIntoImpala(words)

