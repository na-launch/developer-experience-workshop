# Python Kafka Producer / Consumer For OpenShift

Sample console application that connects to your local Kafka instance using Python. Please note, you must have a kafka instance running for this to work. Follow the instructions below 
     
## Usage
```
Usage: python app.py <produce|consume>
```

$~$ 




## Setting Up Environment Variables

> Set the $**KAFKA_BOOTSTRAP_SERVERS** environment variable to change the kafka location

##### Linux
```
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"  
echo $PATH to verify
```  

##### Mac
```
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
Or edit the .bash_profile
echo $PATH to verify
```

##### Windows
```
1. Open the Control Panel
2. Select System
3. Select System Properties / Advanced
4. Select Environment Variables button on the bottom
5. Add the KAFKA_BOOTSTRAP_SERVERS variable here
```

  $~$

