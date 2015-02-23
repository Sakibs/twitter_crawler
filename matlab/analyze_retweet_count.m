tweet_count = tweet_count_DeflatedBalls;
retweet_count = retweet_count_DeflatedBalls;

%Plot simple bar graph of tweets vs retweets
figure; bar(retweet_count,tweet_count);

%Connect points to show rate of tweet count vs retweets
[sorted_retweet_count, indx] = sort(retweet_count);
sorted_tweet_count = tweet_count(indx);
hold on; 
plot(sorted_retweet_count,sorted_tweet_count,'-r','LineWidth',3); 
hold off;

%Analyze tweet count vs retweet count in log log scale
figure; loglog(sorted_retweet_count,sorted_tweet_count,'b-x','LineWidth',3,'MarkerSize',12);
