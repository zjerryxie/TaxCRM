from gluon import *
from gluon.storage import Storage

def ctform(self, columns=2, sectionlist=(), showid=True):
    """ converts a sqlform to columntable format
    organises fields into sections and columns
    each section has a header and group of fields 
    sectionlist is a list of tuples in format (insertbefore, header) """

    # convert sectionlist to list of storage
    sections=[Storage(insertbefore=section[0], header=section[1]) for section in sectionlist]

    # merge sections and fields (note uses table.fields as insertbefore may not be in form)
    items = [field for field in self.table.fields]
    for section in sections:
        items.insert(items.index(section.insertbefore), section)
    # exclude fields not in form.vars (but retain section headers)
    items = [item for item in items if (type(item) is not str) or item in self.custom.widget]
    if not showid and "id" in items:
        del items[items.index("id")]
    
    column=0
    cells=[]
    rows=[]
    tables=[]
    nextindex=1
    for item in items:
        if type(item) is Storage:
            # sectionheader
            if item.header != "":
                rows.append(TR(TH(item.header, _class="ct-sectionheader")))
        else:
            cells.append(TD(self.custom.label[item]+":", _class='ct-label', _width=str(25/float(columns))+'%'))
            cells.append(TD(self.custom.widget[item], _class='ct-data', _width=str(75/float(columns))+'%'))
            column=column+1
        if column==columns or nextindex == len(items) or type(items[nextindex]) is Storage:
            # end of row
            if column>0:
                # add padding cells
                for i in range(columns-column):
                    cells.append(TD())
                    cells.append(TD())
                rows.append(TR(*cells))
            cells=[]
            column=0

        if nextindex == len(items) or type(items[nextindex]) is Storage:
            # end of section
            if len(rows)>0:
                tables.append(TABLE(*rows,_class='ct-table'))
                tables.append(BR())
            rows=[]
        nextindex+=1
    form=CAT(self.custom.begin, CAT(*tables), self.custom.submit, self.custom.end)
    return form
SQLFORM.ctform=ctform