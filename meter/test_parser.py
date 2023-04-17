import os
import tempfile
import unittest
from unittest import mock
from django.core.exceptions import ValidationError
from django.core.management.base import CommandError
from django.db import transaction
from meter.models import Flow
from meter.parser import CsvImporter


class CsvImporterTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to use as test data
        self.file = tempfile.NamedTemporaryFile(delete=False)
        self.file.write(b"123|ABC|2022-01-01|100.0\n")
        self.file.write(b"456|DEF|2022-01-02|200.0\n")
        self.file.close()

    def tearDown(self):
        # Delete the temporary file
        os.unlink(self.file.name)

    def test_validate_row(self):
        importer = CsvImporter(self.file.name)

        # Test a valid row
        row = ['123', 'ABC', '2022-01-01', 100.0]
        expected_flow = Flow(mpan='123', meter='ABC', reading=100.0, filename=self.file.name)
        self.assertEqual(importer.validate_row(row), expected_flow)

        # Test an invalid row
        row = ['123', 'ABC']
        self.assertIsNone(importer.validate_row(row))
        self.assertIn('Invalid row', importer.errors)

    def test_import_csv(self):
        importer = CsvImporter(self.file.name)

        # Test successful import
        with mock.patch.object(Flow, 'full_clean') as mock_full_clean:
            importer.import_csv()
            self.assertEqual(Flow.objects.count(), 2)
            self.assertFalse(importer.errors)
            mock_full_clean.assert_called()

        # Test import with validation error
        with mock.patch.object(Flow, 'full_clean') as mock_full_clean:
            mock_full_clean.side_effect = ValidationError('test error')
            importer.import_csv()
            self.assertEqual(Flow.objects.count(), 0)
            self.assertTrue(importer.errors)
            self.assertIsInstance(importer.errors[0], str)
            mock_full_clean.assert_called()
        
        # Test import with command error
        with mock.patch.object(CommandError, '__init__') as mock_cmd_error:
            importer.errors.append('test error')
            importer.import_csv()
            mock_cmd_error.assert_called_with('Failed to import CSV: [\'test error\']')
