import os, json
import kafka
import urllib.request
import boto3

####################
## Setup Flask Variables
HOST = os.environ.get("SAURON_HTTP_SERVER_HOST", "0.0.0.0")
PORT = os.environ.get("SAURON_HTTP_SERVER_PORT", 6669)
tlsCert = os.environ.get("SAURON_HTTP_SERVER_TLS_CERT", "")
tlsKey = os.environ.get("SAURON_HTTP_SERVER_TLS_KEY", "")

####################
# Setup S3 client
s3SecretPath = os.environ.get("S3_SECRET_PATH", "/var/run/secrets/s3/")
s3EndpointLink = os.environ.get("S3_ENDPOINT_LINK", "s3.us-east-2.amazonaws.com")
verifySSLEnv = os.environ.get("S3_VERIFY_SSL", "False")

verifySSL = False
if verifySSLEnv.lower() == "true":
    verifySSL = True

access_key_id_path = open(s3SecretPath + 'access_key_id', "r")
access_key_secret_path = open(s3SecretPath + 'access_key_secret', "r")
access_key_id = access_key_id_path.read().strip()
access_key_secret = access_key_secret_path.read().strip()

####################
# Setup Kafka client
kafkaTopic = os.environ.get("KAFKA_TOPIC", "gopro-videos")
kafkaEndpoint = os.environ.get("KAFKA_ENDPOINT", "my-cluster-kafka-bootstrap.kafka-cluster.svc.cluster.local:9092")

print("Connecting to: " + kafkaEndpoint)
print("Observing topic: " + kafkaTopic)

consumer = kafka.KafkaConsumer(kafkaTopic, bootstrap_servers=[kafkaEndpoint])

####################
for message in consumer:
    print("===== Received message!")
    print(message)
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    topic = message.topic
    partition = message.partition
    offset = message.offset
    key = message.key # key is also what we use to determine the uploaded bucket/filename
    decodedValue = json.loads(message.value.decode('utf-8')) # value is all the data

    print(decodedValue)

    eventType = decodedValue['EventName']

    record = decodedValue['Records'][0]
    bucket = record['s3']['bucket']['name']
    fileName = record['s3']['object']['key']
    fileType = record['s3']['object']['contentType']
    s3Endpoint = record['responseElements']["x-minio-origin-endpoint"]
    downloadURI = s3Endpoint + "/" + bucket + "/" + fileName

    print("- S3 Endpoint: " + s3Endpoint)
    print("- Bucket: " + bucket)
    print("- Filename: " + fileName)
    print("- URI: " + downloadURI)
    print("- Event Type: " + eventType)

    #print ("%s %s:%d:%d: key=%s value=%s" % (eventType, topic, partition, offset, key, decodedValue))

    # Next, download the file from S3
    urllib.request.urlretrieve(downloadURI, "inf_" + fileName)

    # Execute the inference - image
    # If this is an image, flip the color space

    # Execute the inference - video
    # If this is a video, convert the output to JSON

    # Upload the output to S3
    # Publish the output to Kafka

    # Delete the local file
    # os.remove("inf_" + fileName)