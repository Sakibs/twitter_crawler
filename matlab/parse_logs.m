readDir = 'C:\Users\Naheed\Documents\GitHub\twitter_crawler\logs\';
filename = 'log2_Colts.txt';

f = fopen([readDir filename]);
c = textscan(f,'%s %s %s %s %s', 'Delimiter', '\t');
hashtag = c{1,1};
timeIntervals_cell = c{1,4};
numTweets_cell = c{1,5};

numTweets_arr = zeros(length(numTweets_cell),1);
timeIntervals_arr = zeros(size(numTweets_arr));
for i = 1:length(numTweets_cell)
    split = strsplit(numTweets_cell{i,1},':');
    numTweets_arr(i,1) = str2num(split{1,2});
    split = strsplit(timeIntervals_cell{i,1},':');
    timeIntervals_arr(i,1) = str2num(split{1,2}(2:end-1));
end
numTweets = sum(numTweets_arr);

%Save data to workspace
timeIntervals_arr_Colts = timeIntervals_arr;
numTweets_arr_Colts = numTweets_arr;
numTweets_Colts = numTweets;