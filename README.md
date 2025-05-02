# Python Hello World by Language - App

This is a very quick/simple Python/Flask app that returns  Hello World in the country/language set in your environment variable. The country language code is a two letter code (See Language codes below). The purpose of this application is used for quick testing deployments of Python, you can use this to test environment variables working, deployments into a container. A Dockerfile has been provided so you can test in an image too. 
 
  $~$ 
     

## Setting Up Environment Variables

> Set the $**COUNTRY_CODE** environment variable to change the language
> Set the $**PORT** environment variable to change the port

##### Linux
```
export COUNTRY_CODE="en"
export PORT=8080  
echo $PATH to verify
```  

##### Mac
```
export COUNTRY_CODE="es"
export PORT=8080
Or edit the .bash_profile
echo $PATH to verify
```

##### Windows
```
1. Open the Control Panel
2. Select System
3. Select System Properties / Advanced
4. Select Environment Variables button on the bottom
5. Add the countryCode variable here and choose your two letter language
```

  $~$

## Language Codes accepted 

```
EN=Hello  World!  
ES=¡Hola  Mundo!  
FR=Bonjour  Monde!  
DE=Hallo  Welt!  
ZH=你好  世界!  
JA=こんにちは、世界！  
KO=안녕하세요  세계!  
RU=Привет  мир!  
AR=مرحباً بالعالم!  
PT=Olá  Mundo!  
IT=Ciao  Mondo!  
NL=Hallo  Wereld!  
SV=Hej  Värld!  
NO=Hei  Verden!  
DA=Hej  Verden!  
FI=Hei  Maailma!  
EL=Γειά σου  Κόσμε!  
HE=שלום  עולם!  
TR=Merhaba  Dünya!  
HI=नमस्ते  दुनिया!  
BN=ওহে  বিশ্ব!  
UR=ہیلو، دنیا!  
FA=سلام، دنیا!  
TH=สวัสดี  โลก!  
VI=Xin chào  Thế giới!  
ID=Halo  Dunia!  
MS=Hai  Dunia!  
TL=Kamusta  Mundo!  
SW=Hujambo  Dunia!  
ZU=Sawubona  Mhlaba!  
AF=Hallo  Wêreld!  
AM=ሰላም  ዓለም!  
HU=Helló  Világ!  
CS=Ahoj  Světe!  
SK=Ahoj  Svet!  
PL=Cześć  Świecie!  
RO=Salut  Lume!  
BG=Здравей  Свят!  
HR=Bok  Svijete!  
SR=Здраво  Свете!  
SL=Pozdravljen  Svet!  
MK=Здраво  Свету!  
UK=Привіт  Світ!  
BE=Прывітанне  Свет!  
LT=Labas  Pasauli!  
LV=Sveika  Pasaule!  
ET=Tere  Maailm!  
IS=Halló  Heimur!  
GA=Dia duit  Domhan!  
CY=Helo  Byd!  
GD=Halò  Saoghal!  
BR=Demat  Bed!  
MT=Ħelow  Dinja!  
EU=Kaixo  Mundua!  
GL=Ola  Mundo!  
CA=Hola  Món!  
EO=Saluton  Mondo!  
LA=Salve  Munde!  
HA=Sannu  Duniya!  
YO=Pẹlẹ o  Ayé!  
IG=Ndewo  Ụwa!  
LO=ສະບາຍດີ  ໂລກ!  
KM=សួស្តី  ពិភពលោក!  
MN=Сайн уу  Дэлхий!  
HY=Բարեւ  Աշխարհ!  
KA=გამარჯობა  მსოფლიო!  
AZ=Salam  Dünya!  
KK=Сәлеметсіз бе  Әлем!  
UZ=Salom  Dunyo!  
TG=Салом  Ҷаҳон!  
TK=Salam  Dünýä!  
KU=Silav  Cîhan!  
PS=سلام، نړۍ!  
SI=ආයුබෝවන්  ලෝකය!  
TA=வணக்கம்  உலகம்!  
KN=ಹಲೋ  ವಿಶ್ವ!  
ML=ഹലോ  ലോകം!  
TE=హలో  ప్రపంచం!  
MR=नमस्कार  जग!  
GU=હેલો  વિશ્વ!  
PA=ਸਤ ਸ੍ਰੀ ਅਕਾਲ  ਦੁਨਿਆ!  
NE=नमस्ते  संसार!  
XH=Molo  Lizwe!  
MY=မင်္ဂလာပါ  ကမ္ဘာ!  
TI=ሰላም  ዓለም! 
```