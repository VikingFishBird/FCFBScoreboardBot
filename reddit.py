import praw
print('FAKE COLLEGE FOOTBALL SCOREBOARD BOT v0.1')
print('praw version: {}\n'.format(praw.__version__))

reddit = praw.Reddit('FCFBScoreboardBot')
print("Logged in")
subreddit = reddit.subreddit("FakeCollegeFootball")
