# -*- coding: utf-8 -*-

from twitter_toolkit import *

MAIN_KEYWORDS = ['渋谷', '池袋']
SUB_KEYWORDS = ['カフェ', 'レストラン']
EXCLUDED_KEYWORDS = ['中華']

NEWLINE = "\n"

class TopicGetter(TweetsGetterBySearch):

    def __init__(self, main_keywords=[], sub_keywords=[], excluded_keywords=[]):
        self.main_keywords = main_keywords
        self.sub_keywords = sub_keywords
        self.excluded_keywords = excluded_keywords

        query = self.make_query()
        super(TopicGetter, self).__init__(query)

    def make_query(self):
        queries = []
        for main_keyword in self.main_keywords:
            for sub_keyword in self.sub_keywords:
                query_for_exclusion = ' '.join(["-" + excluded_keyword for excluded_keyword in self.excluded_keywords])
                query = "{0} {1} {2}".format(main_keyword, sub_keyword, query_for_exclusion)
                queries.append(query)

        return ' OR '.join(["({0})".format(query) for query in queries])

    def get_user_type(self, user_dict):
        CORPORATION_KEYWORDS = ['公式']

        def __check_keyword(keywords):

            in_name = False
            in_screen_name = False
            in_description = False
            for keyword in keywords:
                in_name = keyword in user_dict['name'] or in_name
                in_screen_name = keyword in user_dict['screen_name'] or in_screen_name
                in_description = keyword in user_dict['description'] or in_description

            return (in_name, in_screen_name, in_description)

        corporation_result = __check_keyword(['公式'])
        bot_result = __check_keyword(['bot', 'Bot'])
        media_result = __check_keyword(['ニュース', '速報', '新聞', 'トピック', '日刊', 'news', 'topics', 'times'])

        is_corporation = corporation_result[0] or corporation_result[1]
        is_bot = bot_result[0] or bot_result[1] or bot_result[2]
        is_media = media_result[1] or (media_result[0] and media_result[2])

        return (is_corporation, is_bot, is_media)

    def save_tweets(self, file_path, total=-1):
        tweets = getter.collect(total)

        tweets_csv = ''
        for tweet in tweets:
            is_reply = '@' in tweet['text']
            tweet_url = 'https://twitter.com/statuses/' + tweet['id_str']
            is_corporation, is_bot, is_media = self.get_user_type(tweet['user'])
            text_without_newline = tweet['text'].replace("\n", "<newline>")

            csv_elements = [tweet['id_str'],
                            tweet_url,
                            text_without_newline,
                            tweet['created_at'],
                            tweet['retweet_count'],
                            tweet['favorite_count'],
                            int(tweet['retweeted']),
                            int(is_reply),
                            tweet['favorite_count'],
                            tweet['user']['id_str'],
                            tweet['user']['screen_name'],
                            tweet['user']['name'],
                            tweet['user']['followers_count'],
                            tweet['user']['friends_count'],
                            int(tweet['user']['verified']),
                            int(is_corporation),
                            int(is_bot),
                            int(is_media)]

            csv_elements_str = [str(csv_element) for csv_element in csv_elements]
            tweet_csv = ','.join(csv_elements_str)
            tweets_csv += tweet_csv + NEWLINE

        f = open (file_path, 'w')
        f.write(tweets_csv)

if __name__ == '__main__':

    getter = TopicGetter(MAIN_KEYWORDS, SUB_KEYWORDS, EXCLUDED_KEYWORDS)
    print(getter.make_query())

    '''
    count = 0
    for tweet in getter.collect(total = 20):
        print(tweet)
        count += 1
        print ('------ %d' % count)
        print ('{} {} {}'.format(tweet['id'], tweet['created_at'], '@'+tweet['user']['screen_name']))
        print (tweet['text'])
        #
    '''

    getter.save_tweets('test.txt', 100000)
