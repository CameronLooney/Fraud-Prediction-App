
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import requests as re

st.title("Credit Card Fraud Detection App")

st.image('fraud.jpg')

st.write("""
## About
Credit card fraud is a form of identity theft that involves an unauthorized taking of another's credit card information for the purpose of charging purchases to the account or removing funds from it.

**This Streamlit App utilizes a Machine Learning Algorithm to accurately predict wether a Transaction is Fraud or Legitimate**

Click Detection Results in the sidebar to see the results. 


""")

#  'errorbalanceOrg', 'errorbalanceDest', 'HourOfDay',
#        'type_CASH_IN', 'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT',
#        'type_TRANSFER']
st.sidebar.header('User Parameters: ')
step = st.sidebar.slider('Number of Hours it took the Transaction to complete: ')
types = st.sidebar.radio("Transfer Type", ('Cash In','Cash Out', 'Debit', 'Payment', 'Transfer'))
amount = st.sidebar.number_input("Amount in $",min_value=0, max_value=110000)
oldbalanceorg = st.sidebar.number_input('Original Balance Before Transaction was made',min_value=0, max_value=110000)
newbalanceorg= st.sidebar.number_input('New Balance After Transaction was made',min_value=0, max_value=110000)
oldbalancedest= st.sidebar.number_input('Old Balance',min_value=0, max_value=110000)
newbalancedest= st.sidebar.number_input('New Balance',min_value=0, max_value=110000)
errorbalanceORG= st.sidebar.number_input('Original Account Balance Error',min_value=0, max_value=110000)
errorbalanceDest= st.sidebar.number_input('New Account Balance Error',min_value=0, max_value=110000)
hourOfDay= st.sidebar.number_input('New Account Balance Error',min_value=0, max_value=24)


type_CASH_IN= 0
type_CASH_OUT= 0
type_DEBIT= 0
type_PAYMENT= 0
type_TRANSFER = 0

with open('my_model.pkl', 'rb') as file:
    model = pickle.load(file)

if st.sidebar.button("Detection Result"):
    if types == 'Cash In':
        type_CASH_IN = 1
    elif types == 'Cash Out':
        type_CASH_OUT = 1
    elif types == 'Debit':
        type_DEBIT = 1
    elif types == 'Payment':
        type_PAYMENT = 1
    elif types == 'Transfer':
        type_TRANSFER = 1


    values = {
            'step': step,
                'amount': amount,
                'oldbalanceorg': oldbalanceorg,
                'newbalanceorig': newbalanceorg,
                'oldbalancedest': oldbalancedest,
                'newbalancedest': newbalancedest,
                'errorbalanceOrgl': errorbalanceORG,
                'errorbalanceDest': errorbalanceDest,
                'HourOfDay': hourOfDay,
                'type_CASH_IN': type_CASH_IN,
                'type_CASH_OUT': type_CASH_OUT,
                'type_DEBIT': type_DEBIT,
                'type_PAYMENT': type_PAYMENT,
                'type_TRANSFER': type_TRANSFER  }


    df = pd.DataFrame(values, index=[0])
    prediction = model.predict(df)[0]
    prediction_percent = model.predict_proba(df)
    if prediction == 1:
        percent = float(prediction_percent[0][1])
        percent = round((percent *100),2)
        prediction = "Warning: Fraud"
        st.error(prediction)
        st.write("We are {}% confident this transaction is fraud".format(percent))

    else:
        percent = float(prediction_percent[0][0])
        percent = round((percent * 100), 2)
        prediction = "Transaction is Legitimate"
        st.success(prediction)
        st.write("We are {}% confident this transaction is legitimate".format(percent))


