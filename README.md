![image](https://github.com/mytechnotalent/Automation-Framework/blob/main/Automation%20Framework.png?raw=true)

# Automation Framework
An open-source Automation Framework.

## Installation
```bash
git clone https://github.com/mytechnotalent/af.git
```

## Enable SSH (Managed Host)
[Instructions](https://www.raspberrypi.org/documentation/remote-access/ssh)

## Setup Selenium & Chrome Driver (Managed Host)
```bash
sudo apt-get install chromium-chromedriver
sudo apt-get install chromium-browser
sudo apt-get install libatlas-base-dev
pip3 install selenium
pip3 install tweepy
pip3 install pandas
```

## Setup Environment (Control Host)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ssh-keygen
ssh-copy-id pi@192.168.x.x
ssh pi@192.168.x.x
sudo visudo
  %sudo  ALL=(ALL:ALL) NOPASSWD: ALL
```

## Setup Twitter Developer Account
[Website](https://developer.twitter.com)
```
1. Name your Project: hashtag_capture
2. Which best describes you?: Building consumer tools (hobbyist)
3. Describe your new Project: Search hashtags with Ansible integration into an open-source Automation Framework.
4. Add your app: Create a new app instead.
5. Last step, name your App: hashtag_capture_app
6. Click Complete
7. Copy Keys into twitter.py
   consumer_key = "XXXXXXXXXXXXXXXXXXXXX"
   consumer_secret = "XXXXXXXXXXXXXXXXXXXXX"
   access_key = "XXXXXXXXXXXXXXXXXXXXX"
   access_secret = "XXXXXXXXXXXXXXXXXXXXX"
```

## Run
```bash
python af_cli.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
