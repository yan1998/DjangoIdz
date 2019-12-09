import docx
import PyPDF2

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
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)

    @staticmethod
    def read_doc_file():
        return "Извините! Пока не можем прочитать это файл!"
  
    @staticmethod
    def read_pdf_file(file):
        return "Извините! Пока не можем прочитать это файл!"
