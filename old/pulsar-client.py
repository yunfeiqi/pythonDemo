import pulsar

client = pulsar.Client('pulsar://localhost:6650')
consumer = client.subscribe('my-topic', subscription_name='my-topic')

while True:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)

client.close()