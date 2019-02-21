from lib.data import Data
from lib.annual_data import AnnualData
class ModelPdfData():
    #def __init__(self, contents, doc):
    def __init__(self, contents):
        self.contents = contents
        self.data = []

    def prepare_data(self):
        for content in self.contents:
            column_data = self.get_column_data(content)
            if column_data is not None:
                #self.data.append(Data(content, self.doc))
                self.data.append(AnnualData( column_data ))

    def compare_with_keywords(self, keywords):
        for kw in keywords:
            for data in self.data:
                """
                print("*****START****")
                print(data.name)
                print(kw['key'])
                print("*****END******")
                print()
                """
                #print(data.to_json())
                if kw['key'] == data.name:
                    print(f"Keywrod Match -> {data.name}")
                    data.excel_name = kw['value']
                    data.parse = True

    def list_data(self):
        data_list = []
        for data in self.data:
            if data.parse:
                data_list.append(data.to_json())

        print(data_list)

    def get_column_data(self, content):
        content = content.split('  ')
        content = [ ele.strip() for ele in content if ele != "" or ele == "." or ele.strip() != '' or len(ele.strip()) != 0]
        content = [ ele.replace('(', '').replace(')', '') for ele in content if ele != '']
        #content = [ ele.strip for ele in content if ele != "" or ele == "." or ele.strip() != '']
        content_len = len(content)
        if content_len == 3 or content_len == 4 or content_len == 5:
            print("==APPROVED==content-length bw 3 and 5")
            return content
        print("==REJECTED==")
        return None
