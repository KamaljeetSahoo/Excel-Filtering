import streamlit as st
import pandas as pd
import os
import base64

st.title("Excel Filtering")


def save_uploadedfile(uploadedfile):
    with open('data.xlsx', "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="out.csv">Download csv file</a>'
    return href


uploaded_file = st.file_uploader(
    "Choose a file", accept_multiple_files=False, type=['xlsx'])

if uploaded_file:
    save_uploadedfile(uploaded_file)

    df = pd.read_excel('data.xlsx')
    outlet_names = df['RecipientName'].unique()

    final = pd.DataFrame(columns=['RecipientGSTIN', 'RecipientName', 'DocumentNumber', 'DocumentDate',
                         'DocumentValue', 'TaxableAmount', 'GSTRate', 'CESSRate', 'CGST', 'SGST', 'CESS', 'NetLineAmount'])
    for i in range(len(outlet_names)):
        doc_nos = list(df[df['RecipientName'] == outlet_names[i]]
                       ['DocumentNumber'].unique())
        outlet_data = df[df['RecipientName'] == outlet_names[i]]
        for j in range(len(doc_nos)):
            inv_data = outlet_data[outlet_data['DocumentNumber'] == doc_nos[j]]
            gst_rate = list(inv_data['GSTRate'].unique())
            for k in range(len(gst_rate)):
                gst_data = inv_data[inv_data['GSTRate'] == gst_rate[k]]
                d = {
                    'RecipientGSTIN': gst_data['RecipientGSTIN'].unique()[0],
                    'RecipientName': outlet_names[i],
                    'DocumentNumber': gst_data['DocumentNumber'].unique()[0],
                    'DocumentDate': gst_data['DocumentDate'].unique()[0],
                    'DocumentValue': gst_data['DocumentValue'].unique()[0],
                    'TaxableAmount': gst_data['TaxableAmount'].sum(),
                    'GSTRate': gst_data['GSTRate'].unique()[0],
                    'CESSRate': gst_data['CESSRate'].unique()[0],
                    'CGST': gst_data['CGST'].sum(),
                    'SGST': gst_data['SGST'].sum(),
                    'CESS': gst_data['CESS'].sum(),
                    'NetLineAmount': gst_data['NetLineAmount'].sum()
                }
                final = final.append(d, ignore_index=True)
    final.to_csv('out.csv')

    out_df = pd.read_csv('out.csv')
    st.dataframe(out_df)
    st.markdown(get_table_download_link(out_df), unsafe_allow_html=True)
