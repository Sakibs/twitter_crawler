import os
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

#########   list of hashtags to search
queries = ['#SuperBowl','#NFL','#DeflateGate','#DeflatedBalls','#SNL','#Colts']


""" 
Returns HTTP response of Topsy Search API based on query (hashtag), 
start time, end time and limit size (max number of tweets)
"""
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


""" 
Write to file helper
Writes tweets to file line by line
"""
def write_to_file(filepath, tweetlist):
	# clear file contents before overwriting
	with open(filepath, 'w'):
		pass
	# write to file line by line
	f = open(filepath, 'a+')
	for tweet in tweetlist:
		f.write(json.dumps(tweet)+'\n')
	f.close()

""" 
Convert int timestamp to readable date time format
"""
def TStoDT(tstamp):
	return datetime.datetime.fromtimestamp(
        tstamp
    ).strftime('%Y-%m-%d %H:%M:%S')

"""
problem 1
get top tweets for hashtag
"""
def get_top_tweets(hashtag):
	#########   get top 5 tweets for Super Bowl during the time slot of interest
	resp = getTopsyResp(hashtag,mintime,maxtime,5)
	print resp.status, resp.reason

	#########   extract tweets
	resp_content = resp.read()
	ret = json.loads(resp_content)
	top_tweets = ret['response']['results']['list']

	filename = 'top_tweets'+'_'+hashtag[1:]+'.txt'
	filepath = os.path.join('.', 'top_tweets', filename)
	write_to_file(filepath, top_tweets)

"""
crawler
"""
def tweets_crawler():
	timeInterval = 900

	#########	get number of tweets for hashtags in multiple time intervals
	f = open('search_log.txt', 'w')
	for query in queries:
		limitSize = 500
		curtime = mintime
		fromTimes = []
		toTimes = []
		numResults = []
		i = 0
		while (curtime<maxtime):
			resp = getTopsyResp(query,curtime,maxtime,limitSize)
			print resp.status, resp.reason

			#########   extract tweets
			resp_content = resp.read()
			ret = json.loads(resp_content)
			tweets = ret['response']['results']['list']

			#########   build search statistic arrays
			fromTimes.append(mintime)
			toTimes.append(maxtime)
			numResults.append(len(tweets))
			f.write('%r\t\tFrom:%r\t\tTo:%r\t\tNo. Of Results:%r\n' % (query, str(fromTimes[i]), str(toTimes[i]), str(numResults[i]) ))
			
			#########   update array iterator and time interval
			i = i+1
			curtime=curtime+timeInterval
	f.close()


def twitter_crawler_sakib(hashtag):
	limitSize = 500
	timeInterval = 100
	w_start_time = mintime

	# self reference logging
	fromTimes = []
	toTimes = []
	numResults = []
	i = 0 # keep track of number of iterations saved

	logname = 'log'+'_'+hashtag[1:]+'.txt'
	logpath = os.path.join('.', 'logs', logname)
	# start writing log, use a+ if appending data
	log = open(logpath, 'w')

	# start crawling
	while w_start_time < maxtime:
		w_end_time = w_start_time+timeInterval

		# run api query
		resp = getTopsyResp(hashtag, w_start_time, w_end_time, limitSize)
		resp_content = resp.read()
		ret = json.loads(resp_content)
		tweets = ret['response']['results']['list']

		# get number of tweets
		ntweets = len(tweets)

		if(ntweets == 500):
			# half time interval if too many tweets
			print str(i) + ': Halving time, got ' + str(ntweets) + ' tweets'
			timeInterval = timeInterval/2
			# continue and run the query again with smaller time window
			continue
		elif(ntweets < 100):
			print str(i) + ': Doubling time, got ' + str(ntweets) + ' tweets'
			# double time interval if number of tweets is diminishing
			# dont continue, everything is good so far
			timeInterval = timeInterval*2
		else:
			print str(i)
			
		# didnt half time interval and reloop so save current results
		tstart = TStoDT(w_start_time)
		tend = TStoDT(w_end_time)
		log.write('%r\t\tFrom:%r\t\tTo:%r\t\tNo. Of Results:%r\n' % (hashtag, tstart, tend, ntweets))
		
		w_start_time = w_start_time + timeInterval
		# store reference logging vars
		fromTimes.append(tstart)
		toTimes.append(tend)
		i = i+1

# main function declaration
if __name__ == "__main__":
	# time stamp to date time example
	print TStoDT(1422841200)
	print TStoDT(1422845400)

	# part 1
	# get_top_tweets('#SuperBowl')

	# part 2
	print twitter_crawler_sakib('#SuperBowl')