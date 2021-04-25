import pandas as pd

df = pd.read_excel('SALE B2B OCTOBER 2018.xlsx')

df.dropna(axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)

outlet_names = list(df['Outlet Name'].unique())
print(df.dtypes)

final = pd.DataFrame(columns=['Outlet Name', 'Outlet GSTIN Code', 'Invoice No', 'Invoice Date', 'Taxable Line Amt', 'SGST_Tax_Rate', 'SGST_Tax_Value', 'CGST_Tax_Rate', 'Cess_Tax_Rate', 'Total Tax Amount', 'Net Amount'])
print(final)
for i in range(len(outlet_names)):
    invoice_nos = list(df[df['Outlet Name']==outlet_names[i]]['Invoice No'].unique())
    outlet_data = df[df['Outlet Name']==outlet_names[i]]
    for j in range(len(invoice_nos)):
        inv_data = outlet_data[outlet_data['Invoice No']==invoice_nos[j]]
        sgst_rates = list(inv_data['SGST_Tax_Rate'].unique())
        for k in range(len(sgst_rates)):
            sgst_data = inv_data[inv_data['SGST_Tax_Rate']==sgst_rates[k]]
            d = {
                'Outlet Name':outlet_names[i],
                'Outlet GSTIN Code': sgst_data['Outlet GSTIN Code'].unique()[0],
                'Invoice No':sgst_data['Invoice No'].unique()[0],
                'Invoice Date':sgst_data['Invoice Date'].unique()[0],
                'Taxable Line Amt':sgst_data['Taxable Line Amt'].sum(),
                'SGST_Tax_Rate':sgst_data['SGST_Tax_Rate'].unique()[0],
                'SGST_Tax_Value':sgst_data['SGST_Tax_Value'].sum(),
                'CGST_Tax_Rate':sgst_data['CGST_Tax_Rate'].unique()[0],
                'Cess_Tax_Rate':sgst_data['Cess_Tax_Rate'].unique()[0],
                'CGST_Tax_Value':sgst_data['CGST_Tax_Value'].sum(),
                'Cess_Tax_Value':sgst_data['Cess_Tax_Value'].sum(),
                'Total Tax Amount':sgst_data['Total Tax Amount'].sum(),
                'Net Amount':sgst_data['Net Amount'].sum()
                }
            final = final.append(d, ignore_index=True)


final['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
final.to_csv('out.csv')