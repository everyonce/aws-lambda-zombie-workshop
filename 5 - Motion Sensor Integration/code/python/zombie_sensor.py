import boto3
import grovepi
import random
import time

pir_sensor = 8
motion=0
grovepi.pinMode(pir_sensor,"INPUT")

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
mqtt = AWSIoTMQTTClient
mq = mqtt("zombie_sensor")
mq.configureEndpoint("YOUR.ENDPOINT",8883)
mq.configureCredentials("YOUR/ROOT/CA/PATH", "PRIVATE/KEY/PATH", "CERTIFICATE/PATH")
mq.configureAutoReconnectBackoffTime(1, 32, 20)
mq.configureOfflinePublishQueueing(-1)
mq.configureDrainingFrequency(2)
mq.configureMQTTOperationTimeout(5)
mq.connect()

cities = [
    ['London',51.507351,-0.127758],
    ['Las Vegas',36.169941,-115.139830],
    ['New York',40.712784,-74.005941],
    ['Singapore',1.352083,103.819836],
    ['Sydney',-33.867487,151.206990],
    ['Paris',48.856614,2.352222],
    ['Seattle',47.606209,-122.332071],
    ['San Francisco',37.774929,-122.419416],
    ['Montreal',45.501689,-73.567256],
    ['Rio De Janeiro',-22.906847,-43.172896],
    ['Beijing',39.904211,116.407395],
    ['Moscow',55.755826,37.617300],
    ['Buenos Aires',-34.603684,-58.381559],
    ['New Dehli',28.613939,77.209021],
    ['Cape Town',-33.924869,18.424055],
    ['Lagos',6.524379,3.379206],
    ['Munich',48.135125,11.581981]
]


def pickCity():
    city = random.choice(cities)
    return city

def generateAlert():
    city = pickCity()
    message = '{"message":"A Zombie has been detected in ' + city[0] + '!", "longitude":"' + str(city[2]) + '", "latitude":"' + str(city[1]) + '"}'
    print(message)
    mq.publish('zombie-alert',message,1)

def periodicActivity():
    while 1:
        motion=grovepi.digitalRead(pir_sensor)
        if motion==0 or motion==1:
            if motion==1:
                generateAlert()
            else:
                print('--------------------All Clear--------------------')
        time.sleep(1)

periodicActivity()
