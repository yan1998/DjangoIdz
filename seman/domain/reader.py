class Reader:

    @staticmethod
    def read_txt_file(file):
        fileContent = str()
        for chunk in file.chunks():
            fileContent += chunk.decode("utf-8")
        return fileContent

    @staticmethod
    def read_doc_file():
        return "Reading doc file!"
  
    @staticmethod
    def read_pdf_file():
        return "Reading pdf file!"

