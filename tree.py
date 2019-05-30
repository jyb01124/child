
class Rowspan_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Tree:
    def __init__(self, Rowspan):
        self.Root = {
            'name':"Root",
            'rowspan':Rowspan,
            'child':[]
        }

    def add_node(self, Parent, Name, Rowspan):
        data = {'name': Name, 'rowspan': Rowspan, 'child': []}
        Max_num = Parent['rowspan']
        num = 0
        for i in Parent['child']:
            num += i['rowspan']
        if Max_num < (num + Rowspan):
            try:
                raise Rowspan_Error('child들의 rowspan의 합은 부모의 rowspan의 값보다 많을 수 없습니다.')
            except Rowspan_Error as RE:
                print(RE.value)
        else:
            Parent['child'].append(data)

