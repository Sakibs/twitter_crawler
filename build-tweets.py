import pprint
import json
import urllib
import httplib
import json
import datetime, time


#########   create UNIX timestamps
start_date = datetime.datetime(2015,02,01, 17,40,0)
end_date = datetime.datetime(2015,02,01, 18,50,0)
mintime = int(time.mktime(start_date.timetuple()))
maxtime = int(time.mktime(end_date.timetuple()))


#########	Returns HTTP response of Topsy Search API based on query (hashtag), start time, end time and limit size (max number of tweets)
def getTopsyResp(queryString, startTime, endTime, limitSize):
	##########	Topsy API parameters
	API_KEY = '09C43A9B270A470B8EB8F2946A9369F3'
	host = 'api.topsy.com'
	url = '/v2/content/tweets.json'
	
	#########   set query parameters
	params = urllib.urlencode({'apikey' : API_KEY, 'q' : queryString,
		'mintime': str(startTime), 'maxtime': str(endTime),
		'new_only': '1', 'include_metrics':'1', 'limit': limitSize})

	#########   create and send HTTP request
	req_url = url + '?' + params
	req = httplib.HTTPConnection(host)
	req.putrequest("GET", req_url)
	req.putheader("Host", host)
	req.endheaders()
	req.send('')


	#########   get response and print out status
	resp = req.getresponse()
	return resp



#########   get top 5 tweets for Super Bowl during the time slot of interest
resp = getTopsyResp('#SuperBowl',mintime,maxtime,5)
print resp.status, resp.reason

#########   extract tweets
resp_content = resp.read()
ret = json.loads(resp_content)
tweets = ret['response']['results']['list']

#########	write to file
f = open('top_tweets.txt', 'w')
f.write(json.dumps(tweets))
f.close()