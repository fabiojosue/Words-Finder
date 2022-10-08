from distutils import text_file
import PyPDF2
import subprocess
from impala.dbapi import connect

####################################
# POST '/book'
# 1.Convert PDF to .txt File
# 2.Save file in HDFS
# 3.Load HDFS file into Impala Table
####################################
txtFile = 'currentBook.txt'

def pdfToTxt(file):
    specialCharacters = [
                        " ",",",".",":",";",
                        "(",")","!","¡","¿",
                        "?","_","-","'","–",
                        "\"","\n","\t","•","”"
                        ]
    pdfReader = PyPDF2.PdfFileReader(open(file,'rb'))
    numPages = pdfReader.numPages

    with open('./staticFiles/' + txtFile, 'w') as f:

        for i in range(numPages):
            currentPage = pdfReader.getPage(i)
            text = currentPage.extractText()
            for j in range(len(text)):
                #print(text[j])
                if text[j] not in specialCharacters:
                    f.write(text[j].lower())
                else:
                    if text[j-1] not in specialCharacters:
                        f.write("\n")
    

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

def loadIntoImpala(words):
    conn = connect(host = "172.17.0.2", port = 21050)
    cursor = conn.cursor()

    cursor.execute("load data inpath 'hdfs://172.17.0.01:9000/tmp/csv/" + txtFile + "'" + " overwrite into table bd2.book ;") 

    cursor.execute("select count(*) from bd2.book where word='"+words+"';")
    countWords = {"word":cursor.next()[0]}

    cursor.execute("select count(*) from bd2.book;")
    totalWords = {"totalWords":cursor.next()[0]} 

    cursor.close()
    conn.close()

    return countWords | totalWords


def interactBook(words,file):
    pdfToTxt(file)
    run_cmd(['hdfs', 'dfs', '-put', '/home/fabio/bd2-impala/Words-Finder/backend/src/staticFiles/' + txtFile, '/tmp/csv'])
    return loadIntoImpala(words)

