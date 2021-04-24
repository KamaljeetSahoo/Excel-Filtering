import streamlit as st
import pandas as pd

st.title("Excel Filtering")

df = pd.read_csv('data.csv')

df.dropna(axis=0, inplace=True)
df.reset_index(inplace=True)

st.dataframe(df)

outlet_name = st.selectbox('Outlet Name', [None]+list(df['Outlet Name'].unique()))

if outlet_name is not None:
    data = df[df['Outlet Name']==outlet_name]
    st.dataframe(data)

    invoice_num = st.selectbox('Invoice No', [None]+list(data['Invoice No'].unique()))
    if invoice_num is not None:
        invoice_data = data[data['Invoice No']==invoice_num]
        SGST_Tax_Rate = st.selectbox('SGST_Tax_Rate', [None]+list(invoice_data['SGST_Tax_Rate'].unique()))
        if SGST_Tax_Rate is not None:
            sgst_data = invoice_data[invoice_data['SGST_Tax_Rate']==SGST_Tax_Rate]
            st.dataframe(sgst_data)

            d = {
                'Outlet Name':outlet_name,
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
            st.dataframe(pd.DataFrame(data=d, index=[0]))
