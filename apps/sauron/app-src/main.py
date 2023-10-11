import os, json
import kafka
import urllib.request

HOST = os.environ.get("SAURON_HTTP_SERVER_HOST", "0.0.0.0")
PORT = os.environ.get("SAURON_HTTP_SERVER_PORT", 6669)
tlsCert = os.environ.get("SAURON_HTTP_SERVER_TLS_CERT", "")
tlsKey = os.environ.get("SAURON_HTTP_SERVER_TLS_KEY", "")

kafkaTopic = os.environ.get("KAFKA_TOPIC", "gopro-videos")
kafkaEndpoint = os.environ.get("KAFKA_ENDPOINT", "my-cluster-kafka-bootstrap.kafka-cluster.svc.cluster.local:9092")

print("Connecting to: " + kafkaEndpoint)
print("Observing topic: " + kafkaTopic)

#consumer = kafka.KafkaConsumer(kafkaTopic, bootstrap_servers=[kafkaEndpoint], value_deserializer=lambda m: json.loads(m.decode('ascii')))
consumer = kafka.KafkaConsumer(kafkaTopic, bootstrap_servers=[kafkaEndpoint])

for message in consumer:
    print(message)
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    topic = message.topic
    partition = message.partition
    offset = message.offset
    key = message.key # key is also what we use to determine the uploaded bucket/filename
    decodedValue = message.value.decode('utf-8') # value is all the data

    eventType = decodedValue.EventName;

    record = decodedValue.Records[0]
    bucket = record.s3.bucket.name
    fileName = record.s3.object.key
    fileType = record.s3.object.contentType
    s3Endpoint = record.responseElements["x-minio-origin-endpoint"]
    downloadURI = s3Endpoint + "/" + bucket + "/" + fileName

    print("S3 Endpoint: " + s3Endpoint)
    print("Bucket: " + bucket)
    print("Filename: " + fileName)
    print("URI: " + downloadURI)
    print("Event Type: " + eventType)

    print ("%s %s:%d:%d: key=%s value=%s" % (eventType, topic, partition, offset, key, value))

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