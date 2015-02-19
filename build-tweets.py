import os
import json
import urllib
import httplib
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
Write to file helper
Appends tweets to file line by line
"""
def append_to_file(filepath, tweetlist):
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
crawler function to crawl for tweets over a time interval
"""
def twitter_crawler(hashtag, mintime, maxtime, timeInterval):
	limitSize = 500
	w_start_time = mintime

	i = 0 # keep track of number of iterations saved
	logname = 'log'+'_'+hashtag[1:]+'.txt'
	log2name = 'log2'+'_'+hashtag[1:]+'.txt'
	logpath = os.path.join('.', 'logs', logname)
	log2path = os.path.join('.', 'logs', log2name)
	filename = 'tweets'+'_'+hashtag[1:]+'.txt'
	filepath = os.path.join('.', 'tweets', filename)
	# start writing log, use a+ if appending data
	log = open(logpath, 'w')
	log2 = open(log2path, 'w')
	# clear tweet file original contents
	with open(filepath, 'w'):
		pass

	# start crawling
	while w_start_time < maxtime:
		w_end_time = w_start_time+timeInterval
		if(w_end_time>maxtime):
			w_end_time=maxtime
		newTimeInterval = timeInterval
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
			
			# save new time interval for update after writing logs
			newTimeInterval = timeInterval*2
		else:
			print str(i)			


		tstart = TStoDT(w_start_time)
		tend = TStoDT(w_end_time)

		# write tweets to file by appending
		append_to_file(filepath, tweets)

		# didnt half time interval and reloop so save current results
		log.write('%r\tFrom:%r\tTo:%r\tNo. Of Results:%r\n' % (hashtag, tstart, tend, ntweets))
		log2.write('%r\tFrom:%r\tTo:%r\tTimeInterval:%r\tNo. Of Results:%r\n' % (hashtag, str(w_start_time), str(w_end_time), str(timeInterval), ntweets))

		# update variables
		w_start_time = w_start_time + timeInterval
		i = i+1

		# update time interval after updating the start time interval
		timeInterval = newTimeInterval


""" 
Find unique tweets. This function is intended for number 4, this is a work in progress
"""
def unique_tweets(hashtag):
	filename = 'tweets'+'_'+hashtag[1:]+'.txt'
	filepath = os.path.join('.', 'tweets', filename)
	print filepath
	f = open(filepath, 'r')

	tweets_list = []
	conflicts_list = []
	for line in f:
		tweet = json.loads(line)

		title = tweet['title']
		retweet_count = tweet['tweet']['retweet_count']
		retweeted = tweet['tweet']['retweeted']
		# check if tweet is already stored in list
		res = filter(lambda twt: twt['title'] == title, tweets_list)
		# if not stored, store it
		if len(res) < 1:
			new_item = {
				'title': title, 
				'retweet_count': retweet_count, 
				'retweeted': retweeted,
				'count' : 0
			}
			tweets_list.append(new_item)
		# if we found a duplicate tweet store it in conflicts for analysis for now
		else:
			# print "GOT CONFLICT: " + str(len(res))
			# print '\t'+str(retweet_count)+':::'+title.encode('utf8')+'\n'
			item = res[0]
			item['count'] = item['count']+1

			conflict_item = {
				'title': title,
				'retweet_count': retweet_count, 
				'retweeted': retweeted
			}
			conflicts_list.append(conflict_item)


	f.close()

	all_items = json.dumps(tweets_list)

	#### print stuff to debug how retweets are handled
	filename = 'debug'+'_'+hashtag[1:]+'.txt'
	filepath = os.path.join('.', 'tweet_counts', filename)
	f = open(filepath, 'w')
	f.write(all_items)
	f.close()

	all_items = json.dumps(conflicts_list)
	filename = 'conflict'+'_'+hashtag[1:]+'.txt'
	filepath = os.path.join('.', 'tweet_counts', filename)
	f = open(filepath, 'w')
	f.write(all_items)
	f.close()
	##########

	# sum up tweets that were retweet k times
	k_count = []
	for item in tweets_list:
		retweet_count = item['retweet_count']
		res = filter(lambda ct: ct['k'] == retweet_count, k_count)
		if len(res) < 1:
			entry = {
				'k' : retweet_count,
				'count' : 1
			}
			k_count.append(entry)
		else:
			entry = res[0]
			entry['count'] = entry['count'] + 1

	all_items = json.dumps(k_count)
	filename = 'tweet_counts'+'_'+hashtag[1:]+'.txt'
	filepath = os.path.join('.', 'tweet_counts', filename)
	f = open(filepath, 'w')
	f.write(all_items)
	f.close()


"""main function declaration"""
if __name__ == "__main__":
	# time stamp to date time example
	#print TStoDT(1422841200)
	#print TStoDT(1422845400)

	# part 1
	# get_top_tweets('#SuperBowl')

	# part 2
	#timeInterval = 100
	#print twitter_crawler('#NFL',mintime,maxtime,timeInterval)

	unique_tweets('#NFL')