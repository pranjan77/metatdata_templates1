import time
import json
import glob
import os
import uuid
import errno
import subprocess
import zipfile
import shutil
import csv
import numpy
import fileinput
import re

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace as Workspace


class TemplateUtil:

    def _mkdir_p(self, path):
        '''
        _mkdir_p: make directory for given path
        '''
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                pass




    def _copyDirectory(self, src, dst):
        """
        Correctly copy an entire directory
        """
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d) 


    def _generate_report_from_dir(self, index_html_information, params):
        
        objects_created = []

        report_params = {'message': '',
                         'workspace_name': params.get('workspace_name'),
                         'objects_created': [],
                         'file_links': [],
                         'html_links': index_html_information,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                        'report_object_name': 'kb_sample_template_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)
        report_output = {'report_name': output['name'], 'report_ref': output['ref']}
        return report_output



    def _upload_report_directory(self, result_directory):
        report_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(report_directory)
        self._copyDirectory (result_directory, report_directory)

        print (result_directory)
        print (report_directory)



        report_file_path = os.path.join(report_directory, "index.html")

        report_shock_id = self.dfu.file_to_shock({'file_path': report_directory,
                                                  'pack' :"zip"})['shock_id']

        index_html_information = list()
        index_html_information.append({'shock_id': report_shock_id,
                            'name': os.path.basename(report_file_path),
                            'label': os.path.basename(report_file_path),
                            'description': 'Template'})
        return index_html_information



    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        #self.ws = Workspace(self.ws_url, token=self.token)
        self.scratch = config['scratch']

    def run_sample_template_app(self, params):
        # result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        # self._mkdir_p(result_directory)

        result_directory = '/kb/module/test/result'

        index_html_information =  self._upload_report_directory(result_directory)
        report_output =  self._generate_report_from_dir(index_html_information, params)

        returnVal ={}
        returnVal.update(report_output)

        return returnVal

