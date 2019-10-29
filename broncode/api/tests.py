from django.test import TestCase
from .serializers import *
# Create your tests here.

class Code_Submission_TestCase(TestCase):
    def setUp(self):
        pass

    def test_extract_code_output(self):
        language = "C"
        log = "line1\nline2\nline3\nline4\nline5\nline6\nq"
        extractedCode = extract_code_output(log,language)
        self.assertTrue(extractedCode == "q")

        language = "Python3"
        log = "line1\nline2\nq"
        extractedCode = extract_code_output(log,language)
        self.assertTrue(extractedCode == "q")

        language = "InvalidLanguage"
        log = "line1\nline2\nq"
        extractedCode = extract_code_output(log,language)
        self.assertTrue(extractedCode == "")

        language = ""
        log = "line1\nline2\nq"
        extractedCode = extract_code_output(log,language)
        self.assertTrue(extractedCode == "")

        language = "C"
        log = ""
        extractedCode = extract_code_output(log,language)
        self.assertTrue(extractedCode == "")



