import docx
import pdfminer.high_level
import io

class Reader:

    @staticmethod
    def read_txt_file(file):
        fileContent = str()
        for chunk in file.chunks():
            fileContent += chunk.decode("utf-8")
        return fileContent

    @staticmethod
    def read_docx_file(file):
        doc = docx.Document(file)
        fileContent = []
        for para in doc.paragraphs:
            fileContent.append(para.text)
        return '\n'.join(fileContent)

    @staticmethod
    def read_doc_file():
        return "Извините! Пока не можем прочитать это файл!"
  
    @staticmethod
    def read_pdf_file(file):
        fileContent = io.StringIO()
        pdfminer.high_level.extract_text_to_fp(file, fileContent)
        return fileContent.getvalue()
