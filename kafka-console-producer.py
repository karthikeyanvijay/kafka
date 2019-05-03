#!/usr/bin/python
"""
kafka-console-producer.py

Author: Vijay Anand Karthikeyan

"""


from argparse import ArgumentParser
from confluent_kafka import Producer

parser = ArgumentParser(description = 'Kakfa Console Producer in Python', epilog = 'Sample command: %(prog)s --bootstrap.servers=kafkabroker.example.com:6667 --topic=mytopic --security.protocol=SASL_PLAINTEXT --group.id=defaultgroup --sasl.kerberos.principal=user@EXAMPLE.COM --sasl.kerberos.keytab=user.keytab')

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
                            help = 'User Principal for connection', )
paramAuthGrp.add_argument('--sasl.kerberos.keytab', required = True, action = 'store', dest = 'kerberosKeytab', 
                            help = 'Keytab for connection', )
args = parser.parse_args()


conf = {
  'bootstrap.servers': args.bootstrapServers,
  'group.id': args.groupId,
  'session.timeout.ms': args.timeOut,
  'sasl.kerberos.principal': args.kerberosPrincipal,
  'sasl.kerberos.keytab': args.kerberosKeytab,
  'security.protocol': args.securityProtocol,
  'sasl.kerberos.kinit.cmd': 'kinit -k -t "%{sasl.kerberos.keytab}" %{sasl.kerberos.principal}'
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
      # Trigger any available delivery report callbacks from previous produce() calls
      data=raw_input()
      # Asynchronously produce a message, the delivery report callback
      # will be triggered from poll() above, or flush() below, when the message has
      # been successfully delivered or failed permanently.
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