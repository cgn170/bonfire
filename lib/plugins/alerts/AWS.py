#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission

This plugin process AWS alerts configuration files, build a custom cloudformation template with cloudwatch and SNS
configuration 

"""

import os
from lib import SetupLogger
from lib import Settings
from lib import Utils
import yaml
import boto3
import json

# Check if hidden folder exist and create AWS folder inside
_path_deployment_plugin = os.path.join(Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT, "AWS")

# Plugin information, useful to know what it does
plugin_description = "Plugin to process AWS cloudwatch and route53 alerts, check alerts.yml " \
                     "and passwords.yml example files for more information"


# Get plugin description
def get_plugin_description():
    return plugin_description


# Upload file to bucket S3
def upload_file_to_s3(region, aws_access_key_id, aws_secret_access_key, bucket_name, file_path):
    try:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            s3 = boto3.client('s3',
                              region_name=region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)
            s3.upload_file(file_path, bucket_name, filename)
    except Exception as e:
        raise Exception("[error] Could not upload file {0} to S3 bucket {1}, error: {2}"
                        .format(file_path, bucket_name, e))


# Write cloudformation template to file
def write_cloudformation_template_to_file(stack, path):
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

    with open(path, 'w') as outfile:
        yaml.dump(stack, outfile, default_flow_style=False, Dumper=noalias_dumper)

    SetupLogger.logger.debug("Cloudformation template created successfully {}".format(path))


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


# Create cloudformation template for each alert definition file
def create_and_deploy_cloudformation_template_alerts(alert_yml_data=None, aws_keys=None, dry_run=True):
    print("[plugin: AWS] Creating cloudformation alerts template")

    """    
    _aws_account = None
    _category = None
    _sub_category = None
    _monitoring_system = None
    _environment = None
    sns_topic = None
    _namespace = None
    _alarm_name = None
    _alarm_description = None   
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
    """
    _action_enabled = True
    _comparison_operator = None

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

                stack['Description'] += " for {} category, generated by bonfire project".format(_category)

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

                    _alarm_name = "_".join([_category, _sub_category, _environment,
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

                # Write template to file
                stack_name = "{0}-{1}-alerts-stack".format(_account, category)
                stack_file_path = os.path.join(_path_deployment_plugin, stack_name+".yml")
                print("[plugin: AWS] '{0}' stack created in directory '{1}'".format(stack_name, stack_file_path))
                write_cloudformation_template_to_file(stack, stack_file_path)

                # Deploy template
                if not dry_run:
                    # Check if the account exist
                    account_exists = False
                    SetupLogger.logger.debug("Checking if account {} exists in password file".format(_account))
                    for key, val in aws_keys.items():
                        if key.lower() == _account.lower():
                            SetupLogger.logger.debug("Account {} exists".format(_account))
                            account_exists = True
                            break

                    if account_exists:
                        if check_cloudformation_stack(stack_name=stack_name,
                                                      aws_access_key_id=aws_keys[_account]["aws_access_key_id"],
                                                      aws_secret_access_key=aws_keys[_account]
                                                      ["aws_secret_access_key"],
                                                      region=aws_keys[_account]["region"]):
                            update_cloudformation_stack(cloudformation_path=stack_file_path,
                                                        stack_name=stack_name,
                                                        bucket_name=None,
                                                        aws_access_key_id=aws_keys[_account]["aws_access_key_id"],
                                                        aws_secret_access_key=aws_keys[_account]
                                                        ["aws_secret_access_key"],
                                                        region=aws_keys[_account]["region"])
                        else:
                            create_cloudformation_stack(cloudformation_path=stack_file_path,
                                                        stack_name=stack_name,
                                                        aws_access_key_id=aws_keys[_account]["aws_access_key_id"],
                                                        aws_secret_access_key=aws_keys[_account]
                                                        ["aws_secret_access_key"],
                                                        region=aws_keys[_account]["region"])
                    else:
                        print("[plugin: AWS] Account {} does not exist".format(_account))


# Create cloudformation template for the alert dashboard
def create_cloudformation_template_dashboards():
    print("[AWS] Creating cloudformation dashboard template")


# Create cloudformation template to create bucket s3 and nested stacks
def create_cloudformation_template_init_buckets3():
    # Create Header for the YML
    stack = dict(
        AWSTemplateFormatVersion='2010-09-09',
        Description='Bonfire project S3 bucket',
        Resources={
            "S3Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "bonfire-bucket-{}".format(Utils.generate_random_word(10))
                }
            }
        }
    )

    return stack


# Create a cloudformation stack from a S3 bucket or locally
def create_cloudformation_stack(cloudformation_path, stack_name="", bucket_name=None, aws_access_key_id="",
                                aws_secret_access_key="", region=""):
    SetupLogger.logger.debug("[plugin: AWS] Deploying cloudformation template {}".format(cloudformation_path))
    try:

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region)

        cloud_formation = session.client('cloudformation')

        # Check if bucket_name not exist and load cloudformation template locally
        if bucket_name:

            SetupLogger.logger.debug("Trying to invoke template from bucket {}".format(bucket_name))
            response = cloud_formation.create_stack(
                StackName=stack_name,
                TemplateURL=cloudformation_path,
            )

        # If bucket_name exist load cloudformation template from S3 bucket
        else:
            SetupLogger.logger.debug("Bucket name not available, trying to upload with the template "
                                     "local path {}".format(cloudformation_path))
            response = cloud_formation.create_stack(
                StackName=stack_name,
                TemplateBody=json.dumps(Utils.read_yml_file(cloudformation_path)),
            )

        if response["ResponseMetadata"]["HTTPStatusCode"] is 200:
            SetupLogger.logger.debug('Stack {0} created successfully with id: {1}'
                                     .format(stack_name, response['StackId']))
        else:
            SetupLogger.logger.error('Could not create stack {0}, error: {1}'
                                     .format(stack_name, response))

        # print 'Update completed successfully.'
    except Exception as e:
        print('[error] Could not create stack {0}, error: {1}'.format(stack_name, e))


# Update a cloudformation stack from a S3 bucket or locally
def update_cloudformation_stack(cloudformation_path, stack_name="", bucket_name=None, aws_access_key_id="",
                                aws_secret_access_key="", region=""):
    SetupLogger.logger.debug("[plugin: AWS] Deploying cloudformation template {}".format(cloudformation_path))
    try:

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region)

        cloud_formation = session.client('cloudformation')

        # Check if bucket_name not exist and load cloudformation template locally
        if bucket_name:

            SetupLogger.logger.debug("Trying to invoke template from bucket {}".format(bucket_name))
            response = cloud_formation.update_stack(
                StackName=stack_name,
                TemplateURL=cloudformation_path,
            )

        # If bucket_name exist load cloudformation template from S3 bucket
        else:
            SetupLogger.logger.debug("Bucket name not available, trying to upload with the template local path")
            response = cloud_formation.update_stack(
                StackName=stack_name,
                TemplateBody=json.dumps(Utils.read_yml_file(cloudformation_path)),
            )

        if response["ResponseMetadata"]["HTTPStatusCode"] is 200:
            SetupLogger.logger.debug('Stack {0} updated successfully with id: {1}'
                                     .format(stack_name, response['StackId']))
        else:
            SetupLogger.logger.error('Could not update stack {0}, error: {1}'
                                     .format(stack_name, response))

        # print 'Update completed successfully.'
    except Exception as e:
        print('[error] Could not update cloudformation template {0}, error: {1}'
              .format(cloudformation_path, e))


# Delete a cloudformation stack from a S3 bucket or locally
def delete_cloudformation_stack(stack_name="", aws_access_key_id="", aws_secret_access_key="", region=""):
    print("[plugin: AWS] Deleting cloudformation stack {}".format(stack_name))
    try:

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region)

        cloud_formation = session.client('cloudformation')

        # Check if bucket_name not exist and load cloudformation template locally
        if stack_name:
            response = cloud_formation.delete_stack(
                StackName=stack_name,
            )

        if response["ResponseMetadata"]["HTTPStatusCode"] is 200:
            SetupLogger.logger.debug('Stack {0} deleted successfully'
                                     .format(stack_name))
        else:
            SetupLogger.logger.error('Could not delete stack {0}, error: {1}'
                                     .format(stack_name, response))

        # print 'Update completed successfully.'
    except Exception as e:
        SetupLogger.logger.fatal('Could not delete cloudformation stack {0}, error: {1}'
                                 .format(stack_name, e))


# Check if a cloudformation stack exist in an aws account
def check_cloudformation_stack(stack_name="", aws_access_key_id="", aws_secret_access_key="", region=""):
    try:
        SetupLogger.logger.debug("Checking if stack {} already exist".format(stack_name))
        stack_status_list = [
            'CREATE_IN_PROGRESS',
            'CREATE_FAILED',
            'CREATE_COMPLETE',
            'ROLLBACK_IN_PROGRESS',
            'ROLLBACK_FAILED',
            'ROLLBACK_COMPLETE',
            'UPDATE_IN_PROGRESS',
            'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
            'UPDATE_COMPLETE',
            'UPDATE_ROLLBACK_IN_PROGRESS',
            'UPDATE_ROLLBACK_FAILED',
            'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS',
            'UPDATE_ROLLBACK_COMPLETE',
            'REVIEW_IN_PROGRESS',
        ]

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region)

        cloud_formation = session.client('cloudformation')
        paginator = cloud_formation.get_paginator('list_stacks')
        response_iterator = paginator.paginate(StackStatusFilter=stack_status_list)

        for page in response_iterator:
            stack = page['StackSummaries']
            for output in stack:
                if stack_name == str(output['StackName']):
                    SetupLogger.logger.debug('Stack {} exist'.format(stack_name))
                    return True

        SetupLogger.logger.debug("Stack {} does not exist".format(stack_name))
        return False
    except Exception as e:
        print('[error] Could not check cloudformation stack {0}, error: {1}'.format(stack_name, e))


# Get aws access key from file
def get_aws_keys(password_file_path):
    SetupLogger.logger.debug("[plugin: AWS] Extracting aws key from password file")
    return Utils.read_yml_file(password_file_path)


# Deploy function, create and deploy cloudformation template with alerts configuration
def deploy(list_alerts_file, passwords, dry_run):
    # print("Alerts Directory: {}".format(list_alerts_file))
    # print("Password file path: {}".format(password_file_path))

    # Create deployment folder
    Utils.create_folder(overwrite=True, folder_path=_path_deployment_plugin)

    # Create all cloudformation templates
    # Template: Bucket S3 for configuration
    # buckets3_template = create_cloudformation_template_init_buckets3()

    # write_cloudformation_template_to_file(buckets3_template,
    #                                   os.path.join(_path_deployment_plugin, "bonfire_init_buckets3.yml"))

    aws_keys = get_aws_keys(passwords)["AWS"]

    # Deploy template and wait until is finish
    for alert_file in list_alerts_file:
        alert_file_parsed = Utils.read_yml_file(alert_file)
        create_and_deploy_cloudformation_template_alerts(alert_yml_data=alert_file_parsed,
                                                         aws_keys=aws_keys,
                                                         dry_run=dry_run)


# Remove function, remove stacks deployed
def remove(passwords, dry_run):
    print("[plugin: AWS] Removing cloudformation stacks alert")

    # Check if deployment folder exist
    if os.path.exists(_path_deployment_plugin):

        # Read password file
        aws_keys = get_aws_keys(passwords)["AWS"]

        # Get list of cloudformation templates in folder
        deployed_stacks_list = Utils.list_files_in_directory(_path_deployment_plugin)

        for deployed_stack in deployed_stacks_list:
            filename = os.path.basename(deployed_stack)
            # Get account name from filename
            aws_account_stack = filename.split("-")[0]  # -> is always the first string
            stack_name = filename.replace(".yml", "")
            SetupLogger.logger.info("Checking if '{0}' stack exists in AWS account '{1}'"
                                    .format(stack_name, aws_account_stack))
            # Checking if the stack exist
            if check_cloudformation_stack(stack_name=stack_name,
                                          aws_access_key_id=aws_keys[aws_account_stack]["aws_access_key_id"],
                                          aws_secret_access_key=aws_keys[aws_account_stack]
                                          ["aws_secret_access_key"],
                                          region=aws_keys[aws_account_stack]["region"]):
                SetupLogger.logger.info("Stack found, deleting stack '{}'".format(stack_name))
                delete_cloudformation_stack(stack_name=stack_name,
                                            aws_access_key_id=aws_keys[aws_account_stack]["aws_access_key_id"],
                                            aws_secret_access_key=aws_keys[aws_account_stack]
                                            ["aws_secret_access_key"],
                                            region=aws_keys[aws_account_stack]["region"])
            else:
                print("[warning] AWS Cloudformation stack {} does not exists".format(stack_name))

    else:
        print("[error] Directory {} does not exists".format(_path_deployment_plugin))
