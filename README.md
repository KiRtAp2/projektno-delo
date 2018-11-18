# projektno-delo

### Debug strežnik
Preden poženeš, naloži dependencije:\
*NIX: `sudo pip3 install -r requirements.txt`\
Windows: `python -m pip install -r requiremenets.txt`, iz https://www.sqlite.org/download.html potegnes `sqlite-dll-win64-x64-3250300.zip` in `sqlite-tools-win32-x86-3250300.zip`, gres v `Ta Računalnik> Lokalni Disk C` in ustvariš mapo `sqlite`, odzipaš tisti dve mapi in vse kar je noter daš v mapo sqlite. Ko to narediš greš v mapo od projekta in zaženeš `setup_sqlite.cmd`


Za zaganjanje strežnika: (požene se na port 5000)\
*NIX: `./start_server.sh`

Windows: \
    Za naredit tabele in vnest podatke: poženeš `updatedb.cmd`\
    Za zagnat: poženeš `start.cmd`
