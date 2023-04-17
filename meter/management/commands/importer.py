# -*- coding:utf-8 -*-

import logging

from django.core.management.base import BaseCommand

from meter.parser import CsvImporter


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Read a NMI file from file path and store it in the database'
    
    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='The NMI file path to read from')
        
    def handle(self, *args, **options):
        file_path = options['file']
        importer = CsvImporter(file_path)
        error = importer.import_csv() # return CommandError if error
        self.stdout.write(self.style.SUCCESS('Successfully imported CSV'))
        # stdout commandError from error if there is any error
        if error:
            self.stdout.write(self.style.ERROR(error))