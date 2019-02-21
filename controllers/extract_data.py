import logging

from flask import request
from flask import jsonify
from flask_restful import Resource

from controllers.scanned_to_machined import read_scanned_pdf
from exceptions.exceptions_handler import *
from utils import formulate_response
from constant import PDF_UPLOAD_DIRECTORY
from os import path
import os
from service.abby_data_extractor import extract_to_docx
import subprocess


from service.mapping_list import keywords

from service.model_pdf_data import ModelPdfData
from service.update_excel   import ExcelWriter
import uuid

class ExtractData(Resource):

    def post(self):
        try:
            save_path = PDF_UPLOAD_DIRECTORY
            file = request.files['file']

            file_name = file.filename.replace(' ', '_')
            file_name_without_ext = os.path.basename(file_name).split('.')[0]
            file_name_without_ext = file_name_without_ext + "_" + str(uuid.uuid1())
            file_name = file_name_without_ext + path.splitext(file_name)[1]
            doc_dir_location = os.path.join(save_path, file_name_without_ext)
            if not os.path.exists(doc_dir_location):
                os.makedirs(doc_dir_location)
            print(doc_dir_location)
            file_location = os.path.join(doc_dir_location, file_name)
            print(file_location)
            file.save( file_location ) 
            



            #result = read_scanned_pdf(req_payload.get('pdf_path'), req_payload.get('output_dir_location'))
            result = read_scanned_pdf( file_location, doc_dir_location )
            parse_file = result['parse_file']
            template_file = self.create_template( doc_dir_location )

            """
            print("RESULT--->", result)
            stitched_pdf_path = result['stitched_pdf_path']
            template_file_path = os.path.dirname(result['stitched_pdf_path'])
            abby_file_path = os.path.dirname(result['stitched_pdf_path']).replace('pages', 'texts')
            #abby_text_path    = os.path.join(abby_file_path, 'output.txt' )
            abby_text_path    = os.path.join(abby_file_path, 'stitched.txt' )
            print("stitched_pdf_path-->", stitched_pdf_path)
            print("abby_file_path----->", abby_file_path)
            print("abby_text_path----->", abby_text_path)
            #extract_to_docx( stitched_pdf_path, abby_text_path)
            template_file = self.create_template( template_file_path )
            """
            #===START=
            print("==0==", parse_file)
            with open( parse_file, encoding='utf-8' ) as fp:
                contents = fp.readlines()

            print("==1==")
            obj = ModelPdfData(contents)
            obj.prepare_data()

            obj.compare_with_keywords( keywords )
            obj.list_data()
            print("TEMPLATe_FILE**", template_file)
            ew = ExcelWriter( template_file )
            ew.update( obj.data )
            #===END=== 

            result['excel_file_path'] = 'excel_file/' + file_name_without_ext
            result['pdf_file_path']   = 'pdf_file/'   + file_name_without_ext
            return jsonify( {"data": result} )
            #return formulate_response(result, 200, "Successfully Extracted")

        except CustomClassifierException as e:
            print("1***ERROR***", e)
            logging.error("Error {} has occurred in controller".format(e))
            return e.response, e.http_code

        except Exception as e:
            print("2***ERROR***", e)
            logging.error("Error in service = {}".format(e), exc_info=True)
            return InternalServerErrorException(error_code=500,
                                                error_message="Data Extraction failed!").response, 500

        finally:
            logging.info("API Call Finished Successfully - 200")

    def create_template(self, template_path):
        #sample_copy_path = "/Users/shravanc/flask/aditya_birla/ocr-pdf-aditya-malaysia/sample_copy/sample.xlsx"
        sample_copy_path = "/home/ubuntu/aditya_birla/ocr-pdf-aditya-malaysia/sample_copy/sample.xlsx"
        

        a = ['cp', sample_copy_path, template_path]
        template_file = os.path.join(template_path, 'sample.xlsx')
        res = subprocess.check_output(a)
        print(res)
        return template_file

