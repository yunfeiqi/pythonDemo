from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='1.kafka.adh:9092,2.kafka.adh:9092,3.kafka.adh:9092,4.kafka.adh:9092,5.kafka.adh:9092,6.kafka.adh:9092,7.kafka.adh:9092')
future = producer.send('nb-EIP-AI-mas2aio_rc', b'hello world')
future.get()