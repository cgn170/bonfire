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
import yaml


# Create sns topics
def check_sns_topic(topic_arn_list, category):

    # Dict of the topic resources
    topics = []
    topic_resources = []

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
            _sns_topic_ref = topic_arn
        else:
            # logger.info('SNS topic "{}" doesn\'t exist and will be create'.format(topic_arn))
            _sns_topic_name = "{0}-sns-topic-{1}".format(category, Utils.generate_random_word(5))
            # Update topic name with the correct
            _sns_topic_name_ref = _sns_topic_name.replace("-", "")
            _sns_topic_ref = "!Ref {}".format(_sns_topic_name_ref)

            sns_topic_resource = {
                _sns_topic_name_ref: {
                    "Type": "AWS::SNS::Topic",
                    "Properties": {
                        "DisplayName": topic_arn,
                        "TopicName": _sns_topic_name
                    }
                }
            }

            # Add resources
            topic_resources.append(sns_topic_resource)
            SetupLogger.logger.debug('SNS Topic {} added to Cloudformation Template.'.format(_sns_topic_name))
        # Add topic ref
        topics.append(_sns_topic_ref)

        # Check if any suscriptions exist
        if subscriptions is not None:
            for subscription in subscriptions:
                _suscription_name = "{0}-suscription-{1}".format(category, Utils.generate_random_word(5))

                # Update topic name with the correct
                _suscription_name_ref = _suscription_name.replace("-", "")

                subscription_resource = {
                    _suscription_name_ref: {
                        "Type": "AWS::SNS::Subscription",
                        "Properties": {
                            "Endpoint": subscription["Endpoint"],
                            "Protocol": subscription["Protocol"],
                            "TopicArn": _sns_topic_ref
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
        Description='Monitoring alert stack',
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

                stack['Description'] += " for {} category, created by Bonfire Project".format(_category)

                # Check if the SNS Topic exist
                _sns_topic_list = check_sns_topic(alert_yml_data[_category][_monitoring_system]['SNS'], category)

                for sns_resource in _sns_topic_list['resources']:
                    for key, val in sns_resource.items():
                        stack['Resources'][key] = val

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
                    _ok_action = list(_sns_topic_list['topics'])
                    _alarm_action = list(_sns_topic_list['topics'])
                    _dimensions = alert['Dimensions']
                    _insufficient_data = list(_sns_topic_list['topics'])

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
                # Create new object noalias_dumper and disable aliases by
                # overwrite the method ignore_aliases
                # from here
                noalias_dumper = yaml.dumper.SafeDumper
                noalias_dumper.ignore_aliases = lambda self, data: True
                # Create yaml dumps in memory of the template
                stack_yml = (yaml.dump(
                    stack,
                    default_flow_style=False,
                    Dumper=noalias_dumper)).replace('\'', '')

    print(stack_yml)


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

