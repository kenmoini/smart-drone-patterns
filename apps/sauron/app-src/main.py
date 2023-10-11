import os
import kafka

HOST = os.environ.get("SAURON_HTTP_SERVER_HOST", "0.0.0.0")
PORT = os.environ.get("SAURON_HTTP_SERVER_PORT", 6669)
tlsCert = os.environ.get("SAURON_HTTP_SERVER_TLS_CERT", "")
tlsKey = os.environ.get("SAURON_HTTP_SERVER_TLS_KEY", "")

kafkaTopic = os.environ.get("KAFKA_TOPIC", "gopro-videos")
kafkaEndpoint = os.environ.get("KAFKA_ENDPOINT", "my-cluster-source-kafka-bootstrap.kafka-cluster.svc.cluster.local:9092")

consumer = kafka.KafkaConsumer(bookstrap_servers=kafkaEndpoint, topics=kafkaTopic)

for msg in consumer:
    print (msg)