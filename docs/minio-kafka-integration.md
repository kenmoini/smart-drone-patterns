# Minio Event Destination with Kafka

All this, *and more*, is handled by the Minio Init Script in the paired Kubernetes Job.

## Unified Topic Integration

- Identifier: `my-kafka-cluster`
- Brokers: `my-cluster-kafka-brokers.kafka-cluster.svc.cluster.local:9092`
- Topic: `s3-uploads`
- Version: `3.5.0`

Restart the server (box at the top of the web page).

Finally, go to the Bucket and create an Event Subscription for PUTs/GETs/DELETEs.

## Individual Topic<>Bucket Integration

Make sure to create a Topic per-bucket, ie a `minio-gopro-videos` Topic for a `gopro-videos` Bucket.

- Identifier: `my-kafka-cluster-gopro-videos`
- Brokers: `my-cluster-kafka-brokers.kafka-cluster.svc.cluster.local:9092`
- Topic: `minio-gopro-videos`
- Version: `3.5.0`

Rinse & repeat per topic/bucket combo.

Restart the server (box at the top of the web page).

Finally, go to the Bucket and create an Event Subscription for PUTs/GETs/DELETEs that targets that unique Identifier.

## Minio Audit Topic Integration

Minio also has the ability to ship audit logs to Kafka - kinda handy in a way, why not?

Create a Kafka Topic like `minio-audits`.

In the Minio dashboard under **Settings > Audit Kafka**

- Enable: True
- Brokers: `my-cluster-kafka-brokers.kafka-cluster.svc.cluster.local:9092`
- Topic: `minio-audits`
- Version: `3.5.0`