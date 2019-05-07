#!/usr/bin/python
"""
kafka-console-producer.py

Author: Vijay Anand Karthikeyan

"""

import sys
from argparse import ArgumentParser
from confluent_kafka import Producer

parser = ArgumentParser(description = 'Kakfa Console Producer in Python')

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
  'session.timeout.ms': args.timeOut,
  'sasl.kerberos.principal': args.kerberosPrincipal,
  'sasl.kerberos.keytab': args.kerberosKeytab,
  'security.protocol': args.securityProtocol,
  'sasl.kerberos.kinit.cmd': kinitCommand
}
 
p = Producer( ** conf)
 
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

try:
  while 1 == 1:
      data=raw_input()
      p.produce(args.kafkaTopic, data.encode('utf-8'), callback=delivery_report)
      #p.poll(0)
      # Produce message synchronously
      p.flush()
except KeyboardInterrupt:
    print('\nExiting send mode.. waiting all messages to sent!')
 
# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
print('\nProgram Complete!')