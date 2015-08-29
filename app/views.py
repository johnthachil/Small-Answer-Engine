from flask import Flask, render_template, request, url_for
from urllib2 import urlopen
from bs4 import BeautifulSoup
from textblob import TextBlob
import wolframalpha


import requests


from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/result/', methods=['POST','GET'])
def result():
    gotname=request.form['yourname']
    radiobtn=request.form['group1']
    if(radiobtn=="red"):
        print radiobtn
        ainput = gotname
        aplus = "+"
        aword = ""

        words = ainput.split()
        length= int(len(words))

        for i in range(0,length):
            if(i == (length-1)):
                aword=aword+words[i]
            else:
                aword=aword+words[i]+aplus
        aflip="http://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords="
        afinal=aflip+aword
        ################
        asoup1 = BeautifulSoup(urlopen(afinal).read())
        if not asoup1.find_all(attrs={'class': 'a-fixed-left-grid'}):
            list=["PRODUCT NOT FOUND"]
            finalv=0
            return render_template('result.html', newname=list,option="ama",fin=finalv)

        else:

            for item in asoup1.find_all(attrs={'class': 'a-fixed-left-grid'}):
                for link in item.find_all('a'):
                    acapture=link.get('href')

                    break
                break

            #####
            if acapture is None:
                return "bad"
            asoup2 = BeautifulSoup(urlopen(acapture).read())

            for item in asoup2.find_all(attrs={'id': 'acrCustomerReviewLink'}):
                areview=item.get('href')
                break

            sample="http://www.amazon.in"
            afinalreview=sample+areview
            print "REIVIEW:",afinalreview

            amarkup = requests.get(afinalreview)
            asoup2 = BeautifulSoup(amarkup.text)
            amarkup.close()

            reviewTextSoup = asoup2.select('div.reviewText')
            list=[]
            p=0
            n=0
            for x in range(0, 10):
                reviewText = reviewTextSoup[x].get_text()
                #print "[" + str(x) + "]" + reviewText
                blob = TextBlob(reviewText)
                verdict = blob.sentiment
                if verdict.polarity > 0:
                    p=p+10
                else:
                    n=n+10
                zen=TextBlob(reviewText)
                list.append(reviewText)

            str1 = ''.join(list)
            print str1
            blob = TextBlob(str1)
            verdict = blob.sentiment
            OldRange = (1 - (-1))  
            NewRange = (5 - 0)  
            finalv = (((verdict.polarity - (-1)) * NewRange) / OldRange) + (0)

            for sentence in zen.sentences:
                list.append(sentence)        
            return render_template('result.html', newname=list,option="ama",fin=finalv,postive=p,negative=n)


    elif(radiobtn=="yellow"):
        print "enter yahoo"
        url1 = "https://in.answers.yahoo.com/search/search_result?fr=uh3_answers_vert_gs&type=2button&p="
        s = gotname
        q = "%20"
        w = ""
        words = s.split()
        for word in words:
            w=w+word+q
        url=url1+w

        #print url

        ##################
        soup = BeautifulSoup(urlopen(url).read())

        for element in soup.findAll('li'):
            text=(element.get('id'))

        #    text1=str(text)
            if(text != None):
                if(text[0]=="q"):
                    newtext = str(text)
                    newtext = newtext[2:]
                    break

        #print newtext


        ###############

        urlold = 'https://in.answers.yahoo.com/question/index?qid='
        url = urlold+newtext
        #print url
        markup = requests.get(url)
        soup = BeautifulSoup(markup.text)
        markup.close()
        list=[]
        reviewTextSoup = soup.select('span.ya-q-full-text')
        print "-----------------------------------------------------------------------------------------------"

        for x in range(0,1):
            reviewText = reviewTextSoup[x].get_text()
            zen=TextBlob(reviewText)
        for sentence in zen.sentences:
                 list.append(sentence)
        return render_template('result.html', newname=list, option="yah")
    elif(radiobtn=="alpha"):
        client = wolframalpha.Client("W2W352-UW5JRYY26E")
        res = client.query(gotname)
        list=[]
        print "list created\n\n"
        if len(res.pods)>0:
            for i in range (0,len(res.pods)):
                pod = res.pods[i]
                print pod.title
                list.append(pod.text)
            return render_template('result.html', newname=list)
        else:
            list[0]="BAD QUERY"
            return render_template('result.html', newname=list)


    elif(radiobtn=="movie"):
        ainput = gotname
        aplus = "_"
        aword = ""

        words = ainput.split()
        length= int(len(words))
        for i in range(0,length):
            if(i == (length-1)):
                aword=aword+words[i]
            else:
                aword=aword+words[i]+aplus

        final="http://www.rottentomatoes.com/m/"+aword+"/reviews/"
        print final

        amarkup = requests.get(final)
        asoup2 = BeautifulSoup(amarkup.text)
        amarkup.close()
        if not asoup2.select('div.the_review'):
            list=["WRONG MOVIE NAME"]
            finalv=0
            return render_template('result.html', newname=list,option="ama",fin=finalv)
        else:
            reviewTextSoup = asoup2.select('div.the_review')
            list=[]
            n=0
            p=0
            for x in range(0, 10):
                reviewText = reviewTextSoup[x].get_text()
                #print "[" + str(x) + "]" + reviewText
                blob = TextBlob(reviewText)
                verdict = blob.sentiment
                if verdict.polarity > 0:
                    p=p+10
                else:
                    n=n+10
                zen=TextBlob(reviewText)
                list.append(reviewText)

            str1 = ''.join(list)
            print str1
            blob = TextBlob(str1)
            verdict = blob.sentiment
            OldRange = (1 - (-1))  
            NewRange = (5 - 0)  
            finalv = (((verdict.polarity - (-1)) * NewRange) / OldRange) + (0)

            for sentence in zen.sentences:
                list.append(sentence)

            return render_template('result.html', newname=list,option="ama",fin=finalv,postive=p,negative=n)

    else:
        return "WRONG"
