#!/usr/bin/python

# Copyright: (c) 2021, Kevin Thomas <kevin@mytechnotalent.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: twitter

short_description: Twitter module.

version_added: "1.0"

description:
    - "Twitter module that interfaces with the Tweepy module which will extract tweets and geolocations based 
       on a given hashtag."

options:
    hashtag:
        description:
            - This is the hashtag to query.
        required: true
    date_since:
        description:
            - This is the date range to start capturing tweets.
        required: true
    number_of_tweets:
        description:
            - This is the number of tweets to capture.
        

extends_documentation_fragment:
    - (none)

author:
    - Kevin Thomas (@mytechnotalent)
'''

EXAMPLES = '''
# Pass in a hashtag
- name: Test twitter
  twitter:
    hashtag: '#ansible'
    data_since: '2021-03-13'
    number_of_tweets: 10
  register: test
  vars:
    ansible_python_interpreter: '/usr/bin/python3'
'''

RETURN = '''
element_result:
    description: The latest tweets and geolocation of a particular hashtag.
    type: str
    returned: always
'''


from ansible.module_utils.basic import AnsibleModule

import tweepy
import pandas as pd


def __scrape(hashtag, date_since, number_of_tweets):
    # perform data extraction and return response
    # enter your own credentials obtained
    # from your developer account
    consumer_key = "XXXXXXXXXXXXXXXXXXXXX"
    consumer_secret = "XXXXXXXXXXXXXXXXXXXXX"
    access_key = "XXXXXXXXXXXXXXXXXXXXX"
    access_secret = "XXXXXXXXXXXXXXXXXXXXX"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    all_tweets = ()
    # # create DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])
    # use .Cursor() to search through twitter for the required tweets
    # the number of tweets can be restricted using .items(number of tweets)
    tweets = tweepy.Cursor(api.search, q=hashtag, lang='en',
                           since=date_since, tweet_mode='extended').items(number_of_tweets)
    # .Cursor() returns an iterable object and each item in
    # the iterator has various attributes that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]
    # counter to maintain tweet count
    i = 1
    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        # retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])
            # Append all the extracted information in the DataFrame
        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet
        all_tweets += (i, ith_tweet)
        i = i + 1
    filename = 'scraped_tweets.csv'
    # we will save our database as a CSV file
    db.to_csv(filename)
    return True


def run_module(module):
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    hashtag = module.params['hashtag']
    date_since = module.params['date_since']
    number_of_tweets = module.params['number_of_tweets']
    element_result = None

    # noinspection PyBroadException
    try:
        element_result = __scrape(hashtag, date_since, number_of_tweets)
    except:
        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        module.fail_json(msg='Can\'t locate element.')

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        element_result=element_result
    )

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = False

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(result=result)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        hashtag=dict(type='str', required=True),
        date_since=dict(type='str', required=True),
        number_of_tweets=dict(type='int', required=True),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args
    )

    run_module(module)


if __name__ == '__main__':
    main()
