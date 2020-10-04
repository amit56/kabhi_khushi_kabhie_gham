from flask import Flask, jsonify, request
from twitter import *
from monkeylearn import MonkeyLearn
import sys
import json

app = Flask(__name__)

@app.route('/tweetSentiments')
def twitterSentimentData():
    #14d0e773e4f183b82d0cf5ae2622fa90926010d0
    #ml = MonkeyLearn('1f8a83ad2bbb93b4074e4b9e6a2cf5d8acbfe7e4')
    ml = MonkeyLearn('14d0e773e4f183b82d0cf5ae2622fa90926010d0')
    model_id = 'cl_pi3C7JiL'

    #-----------------------------------------------------------------------
    # create twitter API object
    #-----------------------------------------------------------------------

    api_key = "8DyszqLCLYaROTiNeusRlDI6C"
    api_key_secret = "mTNbMxyEVyiH27JGcPZaTAv1Ufo01lDiAx9fZlYntdbm0xchI5"

    access_token = "2899810486-Y3oB2YIIQcsJtRg8M7Kqly8TZn8IyOh738PsdOm"
    access_token_secret = "wRbOffiMGsMWoD9JoBWKrQp82nD52MyWbWlZhGVFAgVvD"
    twitter = Twitter(auth = OAuth(access_token, access_token_secret, api_key, api_key_secret))


    monthMapping = dict()
    monthMapping["Jan"] = "01"
    monthMapping["Feb"] = "02"
    monthMapping["Mar"] = "03"
    monthMapping["Apr"] = "04"
    monthMapping["May"] = "05"
    monthMapping["Jun"] = "06"
    monthMapping["Jul"] = "07"
    monthMapping["Aug"] = "08"
    monthMapping["Sep"] = "09"
    monthMapping["Oct"] = "10"
    monthMapping["Nov"] = "11"
    monthMapping["Dec"] = "12"
    
    def getSentimentData(user):
        
        results = twitter.statuses.user_timeline(screen_name = user, count = 25, exclude_replies=True, include_rts=False)

        #-----------------------------------------------------------------------
        # loop through each status item, and print its content.
        #-----------------------------------------------------------------------

        d = dict()
        texts = list()
        first = True

        dates = list()
        for status in results:
            date = status["created_at"]
            splitted = date.split(" ")
            finalDateUSFormat = monthMapping[splitted[1]] + "/" + splitted[2] + "/" + splitted[5]
            if first or True:
                texts.append(str(status["text"].encode("ascii", "ignore"))[2:])
                dates.append(finalDateUSFormat)
                first = False

        sentiments = ml.classifiers.classify(model_id, texts).body
        for i in range(len(sentiments)):
            sentiment = sentiments[i]["classifications"][0]["tag_name"]
            #print (sentiments[i])
            finalDateUSFormat = dates[i]
            if sentiment.lower() == "positive":
                if finalDateUSFormat in d:
                    cur = d[finalDateUSFormat]
                    d[finalDateUSFormat] = (cur[0] + 1, cur[1])
                else:
                    d[finalDateUSFormat] = (1, 0)

            elif sentiment.lower() == "negative":
                if finalDateUSFormat in d:
                    cur = d[finalDateUSFormat]
                    d[finalDateUSFormat] = (cur[0], cur[1] + 1)
                else:
                    d[finalDateUSFormat] = (0, 1)
        
        return jsonify(d)

        #result = ml.classifiers.classify(model_id, data)

        #print(result.body)

    args = request.args
    print(args)
    userID = args['id']
    print(userID)
    return getSentimentData(userID)


if __name__ == '__main__':
    app.run()