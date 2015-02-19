numTweets = [numTweets_Superbowl; numTweets_NFL; numTweets_DeflateGate; numTweets_DeflatedBalls; numTweets_SNL; numTweets_Colts;];
figure; bar(numTweets);

rate_arr_Superbowl = numTweets_arr_superbowl./timeIntervals_arr_superbowl;
rate_arr_NFL = numTweets_arr_NFL./timeIntervals_arr_NFL;

%Plot tweet rate
figure; hold on  
currTime = 0;
for i = 1:length(timeIntervals_arr_superbowl)
    currTime = currTime+timeIntervals_arr_superbowl(i);
    plot(currTime,rate_arr_Superbowl(i),'*');
end

currTime = 0;
for i = 1:length(timeIntervals_arr_NFL)
    currTime = currTime+timeIntervals_arr_NFL(i);
    plot(currTime,rate_arr_NFL(i),'o');
end
hold off;