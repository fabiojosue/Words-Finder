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
txtFile = 'currentBookTest.txt'

def pdfToTxt(file):
    pdfReader = PyPDF2.PdfFileReader(open(file,'rb'))
    numPages = pdfReader.numPages
    currentPage = pdfReader.getPage(numPages-1)
    text = currentPage.extractText()
 
    specialCharacters = [" ",",",".",";","(",")","!","¡","¿","?","_","-","'","\""]
    with open('./staticFiles/' + txtFile, 'w') as f:
        for i in range(len(text)):
            if text[i] not in specialCharacters :
                f.write(text[i].lower())
            else:
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

def loadIntoImpala():
    conn = connect(host = "172.17.0.2", port = 21050)
    cursor = conn.cursor()

    # print(cursor.description)  # prints the result set's schema
    # results = cursor.fetchall()

    cursor.execute("load data inpath 'hdfs://172.17.0.01:9000/tmp/csv/" + txtFile + "'" + " overwrite into table bd2.book ;") 

    cursor.close()
    conn.close()   

# # select call
# # cursor.execute("Select * from db2.book") 
# # for row in cursor:
# #     print(row)

# #insert call
# cursor.execute("insert into db2.book (name) values('{f}')") 



def saveHDFS(file):
    pdfToTxt(file)
    run_cmd(['hdfs', 'dfs', '-put', '/home/fabio/bd2-impala/Words-Finder/backend/src/staticFiles/' + txtFile, '/tmp/csv'])
    loadIntoImpala()
    return{"Success":True}


def test():
    return {
        "Total": 10,
        "hola":10
    }