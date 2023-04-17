# -*- coding:utf-8 -*-
import csv
from django.core.exceptions import ValidationError
from django.core.management.base import CommandError
from django.db import transaction
from meter.models import Flow


class CsvImporter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.errors = []
    
    def validate_row(self, row):
        try:
            mpan = row[0]
            meter = row[1]
            reading = row[3]
        except (ValueError, IndexError):
            self.errors.append(f"Invalid row: {row}")
            return None
        
        return Flow(
            mpan=mpan,
            meter=meter,
            reading=reading,
            filename=self.file_path
        )
    
    @transaction.atomic
    def import_csv(self):
        with open(self.file_path) as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                flow_reading = self.validate_row(row)
                if flow_reading:
                    try:
                        flow_reading.full_clean()
                        flow_reading.save()
                    except ValidationError as e:
                        self.errors.append(f"Validation error: {e}")
        if self.errors:
            return CommandError(f"Failed to import CSV: {self.errors}")
