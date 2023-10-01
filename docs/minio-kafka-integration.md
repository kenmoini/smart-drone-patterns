# Minio Event Destination with Kafka

- Identifier: `my-kafka-cluster`
- Brokers: `my-cluster-kafka-brokers.kafka-cluster.svc.cluster.local:9092`
- Topic: `s3-uploads`
- Version: `3.5.0`

If you want this to be done per bucket/topic, you'll need to create separate Event entities with different Identifiers.

Restart the server (box at the top of the web page).

Finally, go to the Bucket and create an Event Subscription for PUTs/GETs/DELETEs.