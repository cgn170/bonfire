#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

"""
This plugin process AWS alerts configuration files, build a custom cloudformation template with cloudwatch and SNS
configuration 

"""
from lib import Utils
from lib import SetupLogger


# Create sns topics
def check_sns_topic(topic_arn_list, category):

    # Dict of the topic resources

    topics = []
    topic_resources = []

    topic_counter = 0
    suscription_counter = 0

    for topic_arn in topic_arn_list:

        subscriptions = None

        # Check if the topic arn has any suscription
        if type(topic_arn) is dict:
            topic = list(topic_arn.keys())[0]
            subscriptions = list(topic_arn.values())[0]
            topic_arn = topic

        if type(topic_arn) is str:
            topic_arn = topic_arn

        # If arn resource exist query
        # logger.info('Checking if the SNS topic exist: {}'.format(topic_arn))
        if topic_arn.startswith('arn'):
            """
            try:
                response = client.get_topic_attributes(
                    TopicArn=topic_arn
                )
                logger.info('SNS topic "{}" exist! and can be use it'.format(topic_arn))
                SNS_TOPIC_REF = topic_arn
            except Exception as e:
                raise Exception('Error querying SNS Topic: {}'.format(e))
            """
            SNS_TOPIC_REF = topic_arn
        else:
            # logger.info('SNS topic "{}" doesn\'t exist and will be create'.format(topic_arn))
            SNS_TOPIC_NAME = "{0}-SNSTOPIC-{2}".format(category, uniq_value_topic)
            topic_counter += 1
            # Update topic name with the correct
            SNS_TOPIC_NAME_REF = SNS_TOPIC_NAME.replace("-", "")
            SNS_TOPIC_REF = "!Ref {}".format(SNS_TOPIC_NAME_REF)

            sns_topic_resource = {
                SNS_TOPIC_NAME_REF: {
                    "Type": "AWS::SNS::Topic",
                    "Properties": {
                        "DisplayName": topic_arn,
                        "TopicName": SNS_TOPIC_NAME
                    }
                }
            }

            # Add resources
            topic_resources.append(sns_topic_resource)
            logger.info('SNS Topic {} added to Cloudformation Template.'.format(SNS_TOPIC_NAME))

        # Add topic ref
        topics.append(SNS_TOPIC_REF)

        # Check if any suscriptions exist
        if subscriptions is not None:
            for subscription in subscriptions:
                SUSCRIPTION_NAME = "{0}-{1}-SUSCRIPTION-{2}".format(aws_account, category, uniq_value_suscription)
                uniq_value_suscription += 1

                # Update topic name with the correct
                SUBSCRIPTION_NAME_REF = SUSCRIPTION_NAME.replace("-", "")

                subscription_resource = {
                    SUBSCRIPTION_NAME_REF: {
                        "Type": "AWS::SNS::Subscription",
                        "Properties": {
                            "Endpoint": subscription["Endpoint"],
                            "Protocol": subscription["Protocol"],
                            "TopicArn": SNS_TOPIC_REF
                        }
                    }
                }

                # Add resources
                topic_resources.append(subscription_resource)

    return {'topics': topics, 'resources': topic_resources}


# Create cloudformation template for the alert dashboard
def create_cloudformation_template_dashboards():
    print("[AWS] Creating cloudformation dashboard template")


# Deploy cloudformation stack
def deploy_cloudformation_template():
    print("[AWS] Deploying cloudformation ...")


# Create cloudformation template for each alert definition file
def create_cloudformation_template_alerts(alert_yml_data):
    print("[AWS] Creating cloudformation alerts template")
    # Preseting Variables;
    #    _CATEGORY = _category
    #    _ACCOUNT = _account
    #    _REGION = _region
    #    CATEGORY = _category
    _aws_account = None
    _category = None
    _sub_category = None
    _monitoring_system = None
    _environment = None
    _action_enabled = True
    sns_topic = None
    _namespace = None
    _alarm_name = None
    _alarm_description = None
    _comparison_operator = None
    _threshold = None
    _evaluation_period = None
    _period = None
    _metric_name = None
    _statistic = None
    _ok_action = None
    _alarm_action = None
    _dimensions = None
    _treat_missing_data = None
    _severity = None

    # Create Header for the YML
    stack = dict(
        AWSTemplateFormatVersion='2010-09-09',
        Description='Monitoring alert stack created by Bonfire project',
        Resources={}
    )

    # Query all categories inside the yml alert file

    for category in alert_yml_data:
        # Must use
        _category = str(category)

        # Get Monitoring System
        for monitoring_system in alert_yml_data.get(_category):
            # print 'Monitoring System:',  monitoring_system
            _monitoring_system = str(monitoring_system)

            # Check if the monitor tool is AWS
            if _monitoring_system == "AWS":
                _account = str(alert_yml_data[_category][_monitoring_system]['Account'])


                # Add the description of the stack

                stack['Description'] = "Category: {}".format(_category)
                """
                # Check if the SNS Topic exist
                 SNS_TOPICS_LIST = check_sns_topic(YML_DATA[CATEGORY][MONITORING_SYSTEM]['SNS'],
                                                  _ACCOUNT, _CATEGORY)

                for sns_resource in SNS_TOPICS_LIST['resources']:
                    for key, val in sns_resource.items():
                        stack['Resources'][key] = val
                """

                # Loop for each cloudwatch alert definition
                for name, alert in alert_yml_data[_category][_monitoring_system]['Cloudwatch'].items():
                    _namespace = alert['Namespace']
                    _sub_category = alert['Subcategory']
                    _environment = alert['Env']
                    _metric_name = alert['MetricName']
                    _alarm_description = alert['Desc']
                    _severity = alert['Severity']
                    _threshold = alert['Threshold']
                    _evaluation_period = alert['EvaluationPeriods']

                    _period = alert['Period']
                    _statistic = alert['Statistic']

                    # _ok_action = list(SNS_TOPICS_LIST['topics'])
                    _ok_action = ""
                    _alarm_action = ""
                    _dimensions = alert['Dimensions']
                    _insufficient_data = ""

                    if str(alert['Comparator']) == '>':
                        _comparison_operator = 'GreaterThanThreshold'
                    elif str(alert['Comparator']) == '<':
                        _comparison_operator = 'LessThanThreshold'
                    elif str(alert['Comparator']) == '>=':
                        _comparison_operator = 'GreaterThanOrEqualToThreshold'
                    elif str(alert['Comparator']) == '<=':
                        _comparison_operator = 'LessThanOrEqualToThreshold'

                    _alarm_name = "-".join([_category, _sub_category, _environment,
                                            _metric_name, _comparison_operator, str(_threshold),
                                            str(_evaluation_period), _severity])

                    # Check if the variable TreatMissingData exist
                    try:
                        _treat_missing_data = alert['TreatMissingData']
                    # I should improve this ....
                    except Exception as e:
                        _treat_missing_data = 'missing'

                    _alarm_name_cloudformation = (_alarm_name
                                                  .replace('-', '')
                                                  .replace('_', '')
                                                  .replace('.', '')) + Utils.generate_random_word(4)

                    stack['Resources'][_alarm_name_cloudformation] = \
                        {"Type": "AWS::CloudWatch::Alarm",
                         "Properties": {"ActionsEnabled": _action_enabled,
                                        "AlarmActions": _alarm_action,
                                        "AlarmDescription": _alarm_description,
                                        "AlarmName": _alarm_name,
                                        "ComparisonOperator": _comparison_operator,
                                        "Dimensions": _dimensions,
                                        "EvaluationPeriods": _evaluation_period,
                                        "Period": _period,
                                        # ExtendedStatistic = 'String',
                                        "InsufficientDataActions": _insufficient_data,
                                        "MetricName": _metric_name,
                                        "Namespace": _namespace,
                                        "OKActions": _ok_action,
                                        "Statistic": _statistic,
                                        "Threshold": _threshold,
                                        "TreatMissingData": _treat_missing_data
                                        }
                         }
                    SetupLogger.logger.debug(('Alarm {} added to Cloudformation Template.'
                                              .format(_alarm_name)))
    print(stack)


def get_aws_keys(password_file_path):
    print("[AWS] Extracting aws key from password file")


# Main function, everything starts here
def main(list_alerts_file, password_file_path):
    print("Alerts Directory: {}".format(list_alerts_file))
    print("Password file path: {}".format(password_file_path))

    # Loop all available files

    for alert_file in list_alerts_file:

        alert_file_parsed = Utils.read_yml_file(alert_file)

        create_cloudformation_template_alerts(alert_file_parsed)

