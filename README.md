# Notes

Goal: discover and record version message for as many live nodes as we can

Just run it once.

Ignoring: duration of connection, who told us which addresses (topology), 

### Code plan

Should we attempt to prevent duplicates?
* if yes, this would be main thread's job. perhaps workers could just send back (VersionMessage(), AddrMessage()). Main thread can persist VersionMessage and feed any new addresses into the address queue. But it would need to filter out duplicates using sql at this point ...
* I tend to say "no". This is an optimization. Maybe do this if there is time left over ...

Should I even use a queue? How to test a minimal program???

Main thread 
* Start workers
* Seed addresses queue
* loop
    * just needs to read from result queue and save them into sqlite
    * 

Should worker thread add a timestamp?

### SQLITE

Should I make a separate table to store every IP observed? Basically a backup for the queue?

Done
* Eliminate results queues

Next
* create_table
* save_observation

Others
* get_node_count()
* get_protocol_distribution()
    * ipv4, ipv6, tor
    


##### SQL Schema

addresses table: id, host, port

observations table: all attributes of version message, timestamp, perhaps the list of addresses shared?
* an observations table would still allow us the flexibility to crawl multiple times and see what changes ...

what to do when the connection fails? or we can't connect for some reason? just throw out the address or add it to a blacklist? The simplest thing is to only keep track of successes ...

### Logistics Plan

Logistics
* Make a separate server for just me during the presentation. This way we can have massive congestion and the talk still goes well.
* Deploy more than 1 server
* Use a HUGE box
* Tune the [resource limits](https://the-littlest-jupyterhub.readthedocs.io/en/latest/howto/env/server-resources.html)?
* Move the open file limit to like 100000.

### Questions

Should I copy the whole git repository to `/etc/skel`? This way they wouldn't have to do any binder setup ...

### How to set up

[Install "tlj" on Digital Ocean](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/digitalocean.html)

Open terminal

![image](https://the-littlest-jupyterhub.readthedocs.io/en/latest/_images/new-terminal-button3.png)

```
sudo -E pip install --upgrade pip
sudo -E pip install PySocks requests pytest
```

Start Tor and check that it is running

```
sudo netstat -plnt | grep 9050
```

##### Users choose their passwords

```
sudo tljh-config set auth.type firstuseauthenticator.FirstUseAuthenticator 
sudo tljh-config reload
```

##### Anyone can sign up

```
tljh-config set auth.FirstUseAuthenticator.create_users true
tljh-config reload
```

##### Copy Setup.ipynb to /etc/skel

This are the base files everyone gets. I should probably just keep the repo in here ... Then I can `git pull` right before the talk starts and everyone should get up-to-date code ...

### Notes

* [How to reset user passwords](https://github.com/jupyterhub/the-littlest-jupyterhub/blob/ce59e83857c3d86a8c924a49b3ff19f221f78571/docs/howto/auth/firstuse.rst#resetting-user-password)


#####

Python is installed here: /opt/tljh/user/bin/python3