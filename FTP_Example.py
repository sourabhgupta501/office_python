from ftplib import FTP

ftp = FTP('sasprt.dev.qintra.com')
ftp.login(user='aqcbsftp', passwd = 'SFTP2sas18')
ftp.cwd('/gfs/ftp/pub/aqcb/')


def grabFile():

    filename = 'ARMOR_ALL_FW_WKLY_20181015.csv'

    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()
    localfile.close()


def placeFile():

    filename = 'exampleFile.txt'
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

grabFile()
