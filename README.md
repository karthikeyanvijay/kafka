# Kafka Utils
Use these scripts to interact with the Kafka cluster. Instead of using Zookeeper based authentication, these script uses python API and can work with Kerberos ticket from ticket cache or can use a keytab.

## Setup Packages
The scripts use the python APIs from https://github.com/confluentinc/confluent-kafka-python. To setup the packages to suppport kerberos, use the following steps.

```
yum install -y epel-release && \
	yum install -y curl krb5-workstation cyrus-sasl-gssapi gcc && \
	yum install -y python-devel python-pip && \
	pip install --upgrade pip
curl https://packages.confluent.io/rpm/5.2/confluent.repo -o /etc/yum.repos.d/confluent.repo && \
	yum install -y librdkafka-devel && \
	pip install --no-binary :all: confluent-kafka
# Setup krb5.conf
```

With the incorrect repository setup, the librdkafka-devel package may get installed from EPEL and may be a lower version. If the correct version of the librdkafka-devel is not installed then the install of confluent-kafka installation will fail. Get the latest repo from [here](https://docs.confluent.io/current/installation/installing_cp/rhel-centos.html#systemd-rhel-centos-install).

### Kafka Admin APIs
Use `kafka-adminapi.py` for admin related functionality

```
# python kafka-adminapi.py
Usage: kafka-adminapi.py <bootstrap-brokers> <operation> <args..>

operations:
 create_topics <topic1> <topic2> ..
 delete_topics <topic1> <topic2> ..
 create_partitions <topic1> <new_total_count1> <topic2> <new_total_count2> ..
 describe_configs <resource_type1> <resource_name1> <resource2> <resource_name2> ..
 alter_configs <resource_type1> <resource_name1> <config=val,config2=val2> <resource_type2> <resource_name2> <config..> ..
 delta_alter_configs <resource_type1> <resource_name1> <config=val,config2=val2> <resource_type2> <resource_name2> <config..> ..
 list [<all|topics|brokers>]
 ```

## Kafka Console Producer
Use `kafka-console-producer.py` to publish messages to the Kafka broker. This script works similar to the kafka-console-producer.sh program which is packaged with the Kafka installation. 

Sample command - `python kafka-console-producer.py --bootstrap.servers=kafkaserver.example.com:6667 --topic=testtopic`

#### Usage
```
# python kafka-console-producer.py  --help
usage: kafka-console-producer.py [-h] --bootstrap.servers BOOTSTRAPSERVERS
                                 --topic KAFKATOPIC
                                 [--security.protocol SECURITYPROTOCOL]
                                 [--group.id GROUPID]
                                 [--session.timeout.ms TIMEOUT]
                                 [--sasl.kerberos.principal KERBEROSPRINCIPAL]
                                 [--sasl.kerberos.keytab KERBEROSKEYTAB]
                                 [--useticketcache]
```

## Kafka Console Consumer
Use `kafka-console-consumer.py` to consume messages from the Kafka broker. This script works similar to the kafka-console-consumer.sh program which is packaged with the Kafka installation.

Sample command - `python kafka-console-consumer.py --bootstrap.servers=kafkaserver.example.com:6667 --topic=testtopic`

#### Usage
```
# python kafka-console-consumer.py --help
usage: kafka-console-consumer.py [-h] --bootstrap.servers BOOTSTRAPSERVERS
                                 --topic KAFKATOPIC
                                 [--security.protocol SECURITYPROTOCOL]
                                 [--group.id GROUPID]
                                 [--sasl.kerberos.principal KERBEROSPRINCIPAL]
                                 [--sasl.kerberos.keytab KERBEROSKEYTAB]
                                 [--useticketcache]
```

## Notes
Tested with only the following conditions  
  - Kafka versions - 1.0, 2.0
  - Only with security.protocol=SASL_PLAINTEXT
