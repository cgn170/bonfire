#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Carlos Noguera (cgn170)
See the file 'LICENSE' for copying permission
"""

import os
import xlsxwriter
import operator
from lib import Utils
from lib import Settings
from lib import SetupLogger


class AlertFile:
    def __init__(self, path, data, parsed, category, tool):
        self.path = path
        self.data = data
        self.parsed = parsed
        self.category = category
        self.tool = tool


# Alert object
class AlertDefinitionData:
    def __init__(self, name, category, subcategory, metric, severity, wi, env):
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.metric = metric
        self.severity = severity
        self.wi = wi
        self.env = env


# Documentation class, contains methods to built alert matrix
class Documentation:

    def __init__(self):

        pass



    # Matrix output to csv
    def output_csv_format(self, matrix, output_file_path):

        # Writing in output file
        try:
            SetupLogger.logger.info('Opening csv file: {}'.format(output_file_path))
            file = open(output_file_path, "w")

            SetupLogger.logger.debug('Writing csv headers')
            file.write("{0},{1},{2},{3},{4},{5},{6}".format('Alarm Name', 'Env', 'Category', 'SubCategory',
                                                            'Metric', 'Severity', 'WI'))
            for item in matrix:
                SetupLogger.logger.debug('Writing alert: {}'.format(item.name))
                file.write(
                    "\n{0},{1},{2},{3},{4},{5},{6}".format(item.name,
                                                           item.env,
                                                           item.category,
                                                           item.subcategory,
                                                           item.metric,
                                                           item.severity, item.wi))
            SetupLogger.logger.info('Closing csv file: {}'.format(output_file_path))
            file.close()
        except Exception as e:
            print("[error] Error writing csv alert matrix: {}".format(e))

    # Matrix output to xlsx
    def output_xlsx_format(self, matrix, output_file_path):
        SetupLogger.logger.info('Opening xlsx file: {}'.format(output_file_path))
        try:
            workbook = xlsxwriter.Workbook(output_file_path)
            worksheet = workbook.add_worksheet('Alert Matrix')
            # Freeze first row
            worksheet.freeze_panes(1, 0)
            # Set format header row
            format_cell_header = workbook.add_format({'bold': True, 'align': 'left'})
            format_cell_header.set_bg_color('#b9c3c9')
            row = 0

            SetupLogger.logger.debug('Writing columns headers')
            title = "Alarm Name"
            worksheet.write(0, 0, title, format_cell_header)
            worksheet.set_column(0, 0, len(title) + 60)

            title = "Env"
            worksheet.write(0, 1, title, format_cell_header)
            worksheet.set_column(1, 1, len(title) + 3)

            title = "Category"
            worksheet.write(0, 2, title, format_cell_header)
            worksheet.set_column(2, 2, len(title) + 3)

            title = "SubCategory"
            worksheet.write(0, 3, title, format_cell_header)
            worksheet.set_column(3, 3, len(title) + 5)

            title = "Metric"
            worksheet.write(0, 4, title, format_cell_header)
            worksheet.set_column(4, 4, len(title) + 10)

            title = "Severity"
            worksheet.write(0, 5, title, format_cell_header)
            worksheet.set_column(5, 5, len(title) + 3)

            title = "WI"
            worksheet.write(0, 6, title, format_cell_header)
            worksheet.set_column(6, 6, (len(title) + 50))

            # Set format header row
            row += 1
            for item in matrix:
                # Simulate autofit
                SetupLogger.logger.debug('Writing row: {}'.format(row))
                worksheet.write(row, 0, item.name)
                worksheet.write(row, 1, item.env)
                worksheet.write(row, 2, item.category)
                worksheet.write(row, 3, item.subcategory)
                worksheet.write(row, 4, item.metric)
                worksheet.write(row, 5, item.severity)
                worksheet.write(row, 6, item.wi)
                row += 1

            SetupLogger.logger.debug('Setting autofilter to columns')
            worksheet.autofilter('A1:G' + str(row))

            SetupLogger.logger.info('Closing xlsx file: {}'.format(output_file_path))
            workbook.close()

        except Exception as e:
            print("[error] Error writing xlsx alert matrix: {}".format(e))

    # Matrix output to wiki format - confluence
    def output_wiki_format(self, matrix, output_file_path):

        SetupLogger.logger.info('Opening wiki file: {}'.format(output_file_path))
        try:
            file = open(output_file_path, "w")

            SetupLogger.logger.debug('Writing wiki headers')
            file.write(
                '||{0}||{1}||{2}||{3}||{4}||{5}||{6}||'.format('Alarm Name', 'Env', 'Category', 'SubCategory',
                                                               'Metric', 'Severity', 'WI'))
            for item in matrix:
                SetupLogger.logger.debug('Writing alert: {}'.format(item.name))
                if item.wi == "NO WI FOUND":
                    file.write(
                        "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(item.name, item.env, item.category,
                                                                 item.subcategory, item.metric, item.severity,
                                                                 item.wi))
                else:
                    file.write(
                        "\n|{0}|{1}|{2}|{3}|{4}|{5}|[Link|{6}]|".format(item.name, item.env, item.category,
                                                                        item.subcategory, item.metric,
                                                                        item.severity, item.wi))
            SetupLogger.logger.info('Closing csv file: {}'.format(output_file_path))
            file.close()
        except Exception as e:
            print("[error] Error writing wiki alert matrix: {}".format(e))

    # Parse cloudwatch alerts
    def parse_cloudwatch_alerts(self, alerts, matrix):
        try:
            for key, value in alerts.data["Cloudwatch"].items():
                _category = alerts.category
                _sub_category = value["Subcategory"]
                _metric = value["MetricName"]
                _severity = value["Severity"]
                _wi = value["WI"]
                _env = value["Env"]
                _comparator = value["Comparator"]
                _period = value["Period"]
                _threshold = value["Threshold"]
                # Category-subcategory-environment-metric-comparator-threshold-evaluation_period-severity
                _alarm_name = "-".join([_category, _sub_category, _env,
                                        _metric, _comparator, str(_threshold),
                                        str(_period), _severity])
                SetupLogger.logger.debug('Added alert: {}'.format(_alarm_name))
                matrix.append(AlertDefinitionData(_alarm_name, _category, _sub_category, _metric,
                                                  _severity, _wi, _env))
        except Exception as e:
            print('[error] Could not parse cloudwatch alerts: {}'.format(e))

    # Parse each
    def create_alert_matrix(self, alert_folder):
        SetupLogger.logger.debug("Creating alert matrix list object with alert_folder '{}'".format(alert_folder))
        matrix = []
        alerts = []
        alert_folder_list = Utils.list_files_in_directory(alert_folder)

        # Add each alert object
        for alert_file_path in alert_folder_list:
            # Parse alert yml file
            alert_file_data = Utils.read_yml_file(alert_file_path)
            if type(alert_file_data) is dict:
                category = list(alert_file_data.keys())[0]
                for tool, val in list(alert_file_data.values())[0].items():
                    alert_file_obj = AlertFile(alert_file_path, val, True, category, tool)
                    alerts.append(alert_file_obj)
                SetupLogger.logger.debug('Alert file loaded: {}'.format(alert_file_path))
            else:
                alert_file_obj = AlertFile(alert_file_path, "", False, "", "")
                alerts.append(alert_file_obj)
                SetupLogger.logger.info('Error loading file: {}'.format(alert_file_path))
        alerts.sort(key=operator.attrgetter('category', 'tool'))  # Sort by category and tool
        if type(alerts) is list:
            for alert in alerts:
                if alert.parsed:
                    try:
                        # Parse AWS alerts
                        if alert.tool.lower() == "aws":
                            self.parse_cloudwatch_alerts(alert, matrix)

                    except Exception as e:
                        print('[error] Could not parsed alert: {}'.format(e))
                else:
                    print("[error] Error parsing file '{}'".format(alert.path))

            # Sort by category and tool
            matrix.sort(key=operator.attrgetter('category', 'subcategory'))
            SetupLogger.logger.info("Number of parsed files: {}".format(len(alerts)))
            SetupLogger.logger.info("Number of alerts found: {}".format(len(matrix)))

        return matrix

    # Here is the logic to deploy all documentation
    def process_documentation_deployment(self, config_file_path, alert_matrix_format, dry_run):

        # Read configuration file
        config_file = Utils.read_yml_file(config_file_path)

        # Check if the configuration file exist
        if config_file is None:
            print("[error] Configuration file not found: {}, exiting ...".format(config_file_path))
            exit(1)

        config = config_file.get('config')

        # Validate if the value exist if don't use default
        if not config.get('alerts_dir', False):
            alerts_dir = Settings.CONFIGURATION_FOLDERS["alerts"].get('folder')
            SetupLogger.logger.debug("Variable alerts_dir not defined, using default value: {}".format(alerts_dir))
        else:
            alerts_dir = config.get('alerts_dir')
            SetupLogger.logger.debug("Variable alerts_dir defined, using value: {}".format(alerts_dir))
        # Validate if the dir is valid
        if not os.path.isdir(alerts_dir):
            SetupLogger.logger.fatal("Alerts directory is not valid, exiting ...")
            exit(1)

        # Validate if the value exist if don't use default
        if not config.get('documentation_dir', False):
            documentation_dir = Settings.CONFIGURATION_FOLDERS["documentation"].get('folder')
            SetupLogger.logger.debug(
                "Variable documentation_dir not defined, using default value: {}".format(documentation_dir))
        else:
            documentation_dir = config.get('documentation_dir')
            SetupLogger.logger.debug("documentation_dir defined, using value: {}".format(documentation_dir))
        # Validate if the dir is valid
        if not os.path.isdir(documentation_dir):
            print("[error] Documentation directory is not valid, exiting ...")
            exit(1)

        # Load path list file documentation from documentation folder
        documentation_list_file = Utils.list_files_in_directory(documentation_dir, "")

        if len(documentation_list_file):
            print("[-] Documentation files found: {}".format(len(documentation_list_file)))
        else:
            print("[warning] No documentation file found, is recommended to use some documentation for each alert "
                  "(Optional) ...")

        # Process each file
        # for documentation_file_path in documentation_list_file:
        #    print(documentation_file_path)

        # Create alert matrix
        print("[-] Creating alert matrix, please wait ...")
        alert_matrix = self.create_alert_matrix(alerts_dir)
        print("[-] Alert matrix created successfully!")
        # Default value is wiki
        if alert_matrix_format is None:
            alert_matrix_format = "wiki"

        matrix_output_path = os.path.join(Settings.CONFIGURATION_HIDDEN_FOLDER_DEPLOYMENT,
                                          "alert_matrix.{}".format(alert_matrix_format))

        print("[-] Writing matrix file {}".format(matrix_output_path))
        if alert_matrix_format == "csv":
            self.output_csv_format(alert_matrix, matrix_output_path)
        elif alert_matrix_format == "xlsx":
            self.output_xlsx_format(alert_matrix, matrix_output_path)
        elif alert_matrix_format == "wiki":
            self.output_wiki_format(alert_matrix, matrix_output_path)
        else:
            print("[error] Format '{}' not valid, use xlsx, csv or wiki".format(alert_matrix_format))