#!/usr/bin/python
"""
kafka-console-consumer.py

Author: Vijay Anand Karthikeyan
"""

import sys
from argparse import ArgumentParser
from confluent_kafka import Consumer

parser = ArgumentParser(description = 'Kakfa Console consumer in Python')

paramKafkaGrp = parser.add_argument_group('paramKafkaGrp', 'Configuration Parameters for Kafka broker')
paramKafkaGrp.add_argument('--bootstrap.servers', required = True, action = 'store', dest = 'bootstrapServers', 
                            help = 'Kafka Broker information with port')
paramKafkaGrp.add_argument('--topic', required = True, action = 'store', dest = 'kafkaTopic', 
                            help = 'Kafka Topic')
paramKafkaGrp.add_argument('--security.protocol', action = 'store', dest = 'securityProtocol', default = 'SASL_PLAINTEXT',
                            help = 'Protocol Used for connection (default: %(default)s)')
paramKafkaGrp.add_argument('--group.id', action = 'store', dest = 'groupId',default = 'defaultgroup',
                            help = 'Group ID (default: %(default)s)')

paramAuthGrp = parser.add_argument_group('paramAuthGrp', 'Parameters for authentication')
paramAuthGrp.add_argument('--sasl.kerberos.principal', required = False, action = 'store', dest = 'kerberosPrincipal', 
                            help = 'User Principal for connection')
paramAuthGrp.add_argument('--sasl.kerberos.keytab', required = False, action = 'store', dest = 'kerberosKeytab', 
                            help = 'Keytab for connection')
paramAuthGrp.add_argument('--useticketcache', required = False, action = 'store_true', dest = 'useTicketCache', default = True,
                            help = 'Use Kerberos ticket from cache (default: %(default)s)')
args = parser.parse_args()

if args.useTicketCache and (args.kerberosKeytab or args.kerberosPrincipal):
    parser.error("--sasl.kerberos.principal and --sasl.kerberos.keytab|--useticketcache are mutually exclusive ...")
    sys.exit(2)

kinitCommand=""
if args.useTicketCache:
    kinitCommand = 'echo -ne ""'
    print("Getting Kerberos ticket from cache...")
else:
    kinitCommand = 'kinit -k -t "'+ args.kerberosKeytab + '" ' + args.kerberosPrincipal

conf = {
  'bootstrap.servers': args.bootstrapServers,
  'group.id': args.groupId,
  'sasl.kerberos.principal': args.kerberosPrincipal,
  'sasl.kerberos.keytab': args.kerberosKeytab,
  'security.protocol': args.securityProtocol,
  'sasl.kerberos.kinit.cmd': kinitCommand
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
