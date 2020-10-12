# apartment_rental
Aplikacija je podijeljena u dva dijela:
 * frontend dio
 * backend dio
 
## Frontend
kako bi aplikacija se mogla pokrenuti prvo je potrebno instalirati 
nodeJS package manager(npm) i node
```
sudo apt update
sudo apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt -y install nodejs
```
Nakon toga i naravno ako je skinuta s GitHUB-a aplikacija, trebalo bi se pozicionirati u nju i direktorij app/
prije pocetka pokretanja frontend aplikacije, trebalo bi se pokrenuti naredba
```  
npm install
``` 
kako bi se ispravno instalirali mozda nedostajuci ili nekompatibilni paketi u lokalni node_modules direktorij.
Ukoliko je sve ispravno i naredba nije javila neki Error
moze se slobodno pokrenuti aplikacija
```
npm run serve
```
server ce se dignuti i javiti u command promptu na kojoj adresi se aplikaciji moze pristupiti, u ovom slucaju(http://localhost:8081/)

## Backend
prije pokretanja je potrebno imati podignuti Postgres9.5 lokalno ili dockerizirano
te rucno kreiranu bazu podataka _apartment_rental_
samo konfiguriranje konekcije prema bazi se moze izvesti u datoteci **backend/db.py**.
Takodjer je potrebno instalirati sve librarye koristeci pip install i _requirements.txt_ datoteku
```
pip install -r requirements.txt
```
Nakon instalacije svih potrebnih backend paketa aplikacija se slobodno moze pokrenuti naredbom
```
python3 app.py
```
takodjer ce server javiti na kojem portu slusa, u ovom slucaju defaultno na (http://127.0.0.1:8000)
