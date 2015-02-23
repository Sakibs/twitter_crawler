readDir = 'C:\Users\Naheed\Documents\GitHub\twitter_crawler\tweet_counts\';
filename = 'tweet_counts_SNL.txt';

f = fopen([readDir filename]);
c = textscan(f,'%s %s', 'Delimiter', ',');
tweet_count_cell = c{1,1};
retweet_count_cell = c{1,2};

tweet_count = zeros(size(tweet_count_cell,1),1);
retweet_count = zeros(size(tweet_count));
for i = 1:size(tweet_count_cell,1)
   
    indx = isstrprop(tweet_count_cell{i,1},'digit');
    indx = find(indx==1);
    tweet_count(i,1) = str2num(tweet_count_cell{i,1}(indx));

    indx = isstrprop(retweet_count_cell{i,1},'digit');
    indx = find(indx==1);
    retweet_count(i,1) = str2num(retweet_count_cell{i,1}(indx));
    
end

%Save data to workspace
tweet_count_SNL = tweet_count;
retweet_count_SNL = retweet_count;
