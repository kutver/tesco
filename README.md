# tesco
Tesco web scraper.

![alt text](https://i.imgur.com/gA4nfNv.png)

![alt text](https://i.imgur.com/XqYJYv4.png)
## Installation
```shell
git clone https://github.com/kutver/tesco.git
```

```shell
cd tesco
```

```shell
# Creating virtual environment.
python -m venv tesco_venv
```

```shell
# Activating virtual environment.

# For Linux:
source tesco_venv/bin/activate

# For Windows:
tesco_venv\Scripts\activate.bat
```

```shell
# Installing required packages 
pip install -r tesco_venv/requirements.txt
```

```shell
cd tesco_root
```

```shell
# Launching the web-app in development environment
python manage.py runserver
```

### A Note:
After the installation, if pages are keep loading but not printing anything, replace `user_agent` variable in `tesco_root/tesco/apps/scraper/models.py` to your own user agent.
Shortcut to your user agent: https://www.google.com/search?q=what+is+my+user+agent
