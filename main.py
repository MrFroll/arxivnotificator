import urllib
import model
import smtplib
import settings
import datetime
import re
import HTMLParser
import sys

from xml.dom import minidom
from xml.sax.saxutils import unescape
from email.mime.text import MIMEText

msg = "Hello Dear Friend!\n\n"
footnote = "Sincerely,\n R.K."

def error_log(ms,e):
    dt = datetime.datetime.now()
    print dt.strftime('%d.%m.%Y %H:%M') + ": %s  The reason is: %s " %(ms, e)

url = 'http://export.arxiv.org/rss/gr-qc'
try:
    xml = minidom.parse(urllib.urlopen(url))
except IOError as e:
    error_log('Cannot open the url.',e)
    sys.exit()
def parse_article(xml, key_authors,  key_words):
    count = 0
    articles = xml.getElementsByTagName('item')
    try:
        result = open("result.txt", "w")
    except IOError as e:
        error_log('Cannot open \'result.txt\' file.',e)
        sys.exit()
    for paper in articles:
        papermodel = model.article()
        title = paper.getElementsByTagName('title')[0]
        papermodel.title = title.childNodes[0].nodeValue

        description = paper.getElementsByTagName('description')[0]
        description = description.childNodes[0].nodeValue
        abstract = re.findall('<.*?>(.*?)<.*?>', description, re.DOTALL)
        for a in abstract:
            papermodel.description = papermodel.description + '\t' + a
        link = paper.getElementsByTagName('link')[0]
        papermodel.link = link.childNodes[0].nodeValue

        creator = paper.getElementsByTagName('dc:creator')[0]
        creator = str(unescape(creator.childNodes[0].nodeValue))
        authors = re.findall('<.*?>(.*?)<.*?>', creator)
        for a in authors:
            # To get a good view of unicode. For example from &#x01ce; to u'\u01ce'
            papermodel.authors.append(HTMLParser.HTMLParser().unescape(a))
        if papermodel.checker(key_authors, key_words):
            count += 1
            papermodel.printToFile(result)
    result.close()
    return count

def send_mail(message):
    dt = datetime.datetime.now()
    try:
        mime = MIMEText(message, 'plain', 'utf-8')
        mime['Subject'] = "Latest arxiv.org news from " + dt.isoformat()
        mime['From'] = settings.sender
        mime['To'] = settings.recipient
        smtp = smtplib.SMTP(settings.server, settings.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(settings.sender, settings.passw)
        smtp.sendmail(settings.sender, settings.recipient, mime.as_string())
        smtp.close()
        print dt.strftime('%d.%m.%Y %H:%M') + ": The mail notification was sent"
    except Exception as e:
        error_log('The email from cannot be send.',e)
        sys.exit()

count = parse_article(xml,settings.keyauthors,settings.keywords)
if count == 0:
    msg = msg + "Unfortunately, today there isn't any articles you find."
elif count == 1:
    msg = msg + "There is one interesting article today:"
else:
    msg = msg + "There are "+str(count)+" interesting article today:"
msg = msg+"\n\n"
fp = open("result.txt", "rb")
msg = msg + fp.read()
fp.close()
msg = msg + footnote

send_mail(msg)