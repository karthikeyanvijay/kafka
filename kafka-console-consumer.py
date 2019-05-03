#!/usr/bin/python
"""
kafka-console-consumer.py

Author: Vijay Anand Karthikeyan
"""

from argparse import ArgumentParser
from confluent_kafka import Consumer

parser = ArgumentParser(description = 'Kakfa Console consumer in Python', epilog = 'Sample command: %(prog)s --bootstrap.servers=kafkabroker.example.com:6667 --topic=mytopic --security.protocol=SASL_PLAINTEXT --group.id=defaultgroup --sasl.kerberos.principal=user@EXAMPLE.COM --sasl.kerberos.keytab=user.keytab')

paramKafkaGrp = parser.add_argument_group('paramKafkaGrp', 'Configuration Parameters for Kafka broker')
paramKafkaGrp.add_argument('--bootstrap.servers', required = True, action = 'store', dest = 'bootstrapServers', 
                            help = 'Kafka Broker information with port')
paramKafkaGrp.add_argument('--topic', required = True, action = 'store', dest = 'kafkaTopic', 
                            help = 'Kafka Topic')
paramKafkaGrp.add_argument('--security.protocol', action = 'store', dest = 'securityProtocol', default = 'SASL_PLAINTEXT',
                            help = 'Protocol Used for connection (default: %(default)s)')
paramKafkaGrp.add_argument('--group.id', action = 'store', dest = 'groupId',default = 'defaultgroup',
                            help = 'Group ID (default: %(default)s)')
paramKafkaGrp.add_argument('--session.timeout.ms', action = 'store', dest = 'timeOut', default = 6000,
                            help = 'Session Timeout (default: %(default)s)')

paramAuthGrp = parser.add_argument_group('paramAuthGrp', 'Parameters for authentication')
paramAuthGrp.add_argument('--sasl.kerberos.principal', required = True, action = 'store', dest = 'kerberosPrincipal', 
                            help = 'User Principal for connection')
paramAuthGrp.add_argument('--sasl.kerberos.keytab', required = True, action = 'store', dest = 'kerberosKeytab', 
                            help = 'Keytab for connection')
args = parser.parse_args()

conf = {
  'bootstrap.servers': args.bootstrapServers,
  'group.id': args.groupId,
  'sasl.kerberos.principal': args.kerberosPrincipal,
  'sasl.kerberos.keytab': args.kerberosKeytab,
  'security.protocol': args.securityProtocol,
  'sasl.kerberos.kinit.cmd': 'kinit -k -t "%{sasl.kerberos.keytab}" %{sasl.kerberos.principal}'
}

c = Consumer( ** conf)

c.subscribe([args.kafkaTopic])

try:
    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print('Received message: {}'.format(msg.value().decode('utf-8')))
except KeyboardInterrupt:
    print('\nExiting...!')

c.close()

print('\nProgram Complete!')
