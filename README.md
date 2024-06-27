## Automated booking
During Covid my local swimming pool employed a system where one had to pre-book swimming lane slots. This measure was introduced to prevent from too many people swimming in one lane at once.

This was tremendously inconvenient to me as the slots would be released at 6am and would usually be booked out by 7am. Not wanting to get up that early every day, I put together a small script to automate the booking for me every morning.

The automation was implemented using Selenium, periodic execution of the script was scheduled using crontab.

## Setup
- Install python (any version above 3.3)
- Install pip
  - macOS:
    - curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    - python3 get-pip.py
- `pip install selenium`
- Download [chromedriver](https://sites.google.com/chromium.org/driver/)
- Change username and password in script
- Give script permission: `chmod a+x`