# Local Setup

Make sure you haver Python 3.6 or higher, as well as the `pip` and `venv` packages installed. Ensure you have Tor running on port 9050 in order for the Tor examples to work. Then:

```
python3 -m venv venv
source venv/bin/activate
pip install PySocks requests jupyter pytest
jupyter notebook
```

If a browser windows doesn't open automatically, copy and paste the URL displayed in your terminal into your browser.

# Setup in the cloud

Follow this [install "tlj" on Digital Ocean](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/digitalocean.html) tutorial

Open terminal:

![image](https://the-littlest-jupyterhub.readthedocs.io/en/latest/_images/new-terminal-button3.png)

## Install some Python packages and Tor

```
sudo -E pip install --upgrade pip
sudo -E pip install PySocks requests pytest
sudo -E apt install tor
```

## Start Tor and check that it is running

```
sudo systemctl start tor.service
sudo netstat -plnt | grep 9050
```

(use `ss` instead of `netstat` if you're on Arch linux ...)

## Users choose their passwords

```
sudo tljh-config set auth.type firstuseauthenticator.FirstUseAuthenticator 
sudo tljh-config reload
```

## Allow anyone to sign up

```
tljh-config set auth.FirstUseAuthenticator.create_users true
tljh-config reload
```

## Clone this repo to /etc/skel

This are the base files everyone gets when they create an account.

## Misc

* [How to reset user passwords](https://github.com/jupyterhub/the-littlest-jupyterhub/blob/ce59e83857c3d86a8c924a49b3ff19f221f78571/docs/howto/auth/firstuse.rst#resetting-user-password)
* Python is installed here: /opt/tljh/user/bin/python3
