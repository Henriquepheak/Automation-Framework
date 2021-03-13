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
    hashtag: 'ansible'
    data_since: 2021-03-13
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

import pandas as pd
import tweepy
from secrets import *


def __launch():
    # allocate headless driver object
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1024x768')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    return driver


def __query(driver, query, url, find_element_by, element, wait):
    # query web and return response
    element_result = None
    driver.get('https://{}'.format(url))
    if find_element_by == 'id':
        # noinspection PyBroadException
        try:
            WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.ID, element))
            )
        except:
            driver.quit()
        element_result = driver.find_element_by_id('{}'.format(element))
    if find_element_by == 'name':
        # noinspection PyBroadException
        try:
            WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((By.NAME, element))
            )
        except:
            driver.quit()
        element_result = driver.find_element_by_name('{}'.format(element))
    if find_element_by == 'xpath':
        # noinspection PyBroadException
        try:
            WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.XPATH, element))
            )
        except:
            driver.quit()
        element_result = driver.find_element_by_xpath('{}'.format(element))
    element_result.send_keys(query)
    element_result.send_keys(Keys.RETURN)
    element_result = driver.find_element_by_xpath('//*').text
    driver.quit()
    return element_result


def run_module(module):
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    query = module.params['query']
    url = module.params['url']
    find_element_by = module.params['find_element_by']
    element = module.params['element']
    timeout = 60
    element_result = None

    # launch headless driver object and store in driver
    driver = __launch()

    # noinspection PyBroadException
    try:
        if query:
            element_result = __query(driver, query, url, find_element_by, element, timeout)
    except:
        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        driver.quit()
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
        query=dict(type='str', required=False),
        url=dict(type='str', required=True),
        find_element_by=dict(type='str', required=True),
        element=dict(type='str', required=True)
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
