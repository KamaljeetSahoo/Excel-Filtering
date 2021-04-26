import pandas as pd

df = pd.read_excel('1 B2B SALE 2019.xlsx')

outlet_names = df['RecipientName'].unique()

final = pd.DataFrame(columns=['RecipientGSTIN', 'RecipientName', 'DocumentNumber', 'DocumentDate', 'DocumentValue', 'TaxableAmount', 'GSTRate', 'CESSRate', 'CGST', 'SGST', 'CESS', 'NetLineAmount'])


for i in range(len(outlet_names)):
    doc_nos = list(df[df['RecipientName']==outlet_names[i]]['DocumentNumber'].unique())
    outlet_data = df[df['RecipientName']==outlet_names[i]]
    for j in range(len(doc_nos)):
        inv_data = outlet_data[outlet_data['DocumentNumber']==doc_nos[j]]
        gst_rate = list(inv_data['GSTRate'].unique())
        for k in range(len(gst_rate)):
            gst_data = inv_data[inv_data['GSTRate']==gst_rate[k]]
            d = {
               'RecipientGSTIN': gst_data['RecipientGSTIN'].unique()[0],
               'RecipientName': outlet_names[i],
               'DocumentNumber': gst_data['DocumentNumber'].unique()[0],
               'DocumentDate': gst_data['DocumentDate'].unique()[0],
               'DocumentValue': gst_data['DocumentValue'].unique()[0],
               'TaxableAmount': gst_data['TaxableAmount'].sum(),
               'GSTRate' : gst_data['GSTRate'].unique()[0],
               'CESSRate' : gst_data['CESSRate'].unique()[0],
               'CGST' : gst_data['CGST'].sum(),
               'SGST' : gst_data['SGST'].sum(),
               'CESS' : gst_data['CESS'].sum(),
               'NetLineAmount' : gst_data['NetLineAmount'].sum()
            }
            final = final.append(d, ignore_index=True)

final.to_csv('out.csv')