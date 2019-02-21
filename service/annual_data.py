class AnnualData():
    def __init__(self, content):
        #print("ANNUAL_DATA-->", content)
        if len(content) == 4:
            print("LENGTH is 4")
            try:
                #print("Trying-->stockin-->1", content)
                int(content[1].replace('a', '').replace('b', ''))
                self.name = content[0]
                self.note = content[1]
                self.val_1 = self.format_number(content[2])
                self.val_2 = self.format_number(content[3])
                #self.name, self.note, self.val_1, self.val_2 = content
            except:
                self.serial, self.name, self.val_1, self.val_2 = content
                #print("Trying-->stockin-->2", self.to_json())
        elif len(content) == 3:
            print("LENGTH is 3")
            self.name, self.val_1, self.val_2            = content
        elif len(content) == 5:
            self.serial, self.name, self.note, self.val_1, self.val_2 = content 

        self.parse = False
        self.excel_name = ""

    def to_json(self):
        try:
            return {"name": self.name, "val_1": self.val_1, "val_2": self.val_2, "excel_name": self.excel_name}
        except:
            return {"name": self.name, "val_1": self.val_1, "val_2": self.val_2}
          
    def format_number(self, number):
        print(f"***{number}***{self.name}")
        if number == 'NIL' or number == "Nil -" or number == '_•' or number == '•-' or number == '._•':
            return '0'
        number = number.replace(' ', '.')
        split_arr = number.split('.')
        whole_number_arr = split_arr[:-1]
        whole_number = ""
        for wn in whole_number_arr:
            whole_number = whole_number + "".join( wn.split(',') )
        
        float_number = whole_number + '.' + split_arr[-1]
        return float_number

