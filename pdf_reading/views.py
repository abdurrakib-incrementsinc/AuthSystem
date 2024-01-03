import io

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import spacy
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from spacy.matcher import Matcher
import os
from .document_similarity import document_token
# Create your views here.


class PdfExtractionView(APIView):
    def get(self, request, *args, **kwargs):  # sourcery skip: use-join
        # # pdf_path = "./resume/resume.pdf"
        # app_base_dir = os.path.dirname(os.path.abspath(__file__))
        # pdf_path = os.path.join(app_base_dir, 'resume', 'resume.pdf')
        # print("path...", pdf_path)
        # text = ""
        # # calling function to extracting text
        # for page in self.extract_text_from_pdf(pdf_path):
        #     text += f'{page}'
        # print(text)
        # name = self.extract_name(text)
        # print("Name...", name)
        # return Response({"Name": name}, status=status.HTTP_200_OK)
        app_base_dir = os.path.dirname(os.path.abspath(__file__))
        document_path1 = os.path.join(app_base_dir, 'resume', 'document.txt')
        document_path2 = os.path.join(app_base_dir, 'resume', 'document2.txt')
        document_token(document_path1, document_path2)
        return Response("hello!", status=status.HTTP_200_OK)

    @staticmethod
    def extract_name(resume_text):
        # load pre-trained model
        nlp = spacy.load('en_core_web_sm')
        # initialize matcher with a vocab
        matcher = Matcher(nlp.vocab)
        nlp_text = nlp(resume_text)
        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}]
        matcher.add('NAME', [pattern])
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, 'rb') as fh:
            # iterate over all pages of PDF document
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                # creating a resoure manager
                resource_manager = PDFResourceManager()

                # create a file handle
                file_handler = io.StringIO()

                # creating a text converter object
                converter = TextConverter(
                    resource_manager,
                    file_handler,
                    codec='utf-8',
                    laparams=LAParams()
                )

                # creating a page interpreter
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )

                # process current page
                page_interpreter.process_page(page)

                # extract text
                yield file_handler.getvalue()

                # close open handles
                converter.close()
                file_handler.close()


