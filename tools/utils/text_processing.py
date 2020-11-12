import re
from collections import namedtuple
import numpy as np



def text_processing(loc,text):

  #define the dictionary 
  dict_val = dict()

  if(loc["id"]=="service_bill"):
    #define the bill heading
    head_1 = text.split('\n')[0] 
    head_2 = text.split('\n')[-2].split(" ")[0]
    final_head = " ".join([head_1,head_2])

    dict_val.update({"Heading":final_head})


  if(loc["id"]=="bill summary"):

    data_list = text.split('\n')

    for i_sentence in data_list :

      if (any(map(lambda word: word in i_sentence, ["Bill Date"]))):
        bill_date = i_sentence.translate({ord("|"): None}).split(" ")
        bill_date = list(filter(None, bill_date))

        dict_val.update({"Bill Date":bill_date[-1]})

      if (any(map(lambda word: word in i_sentence, ["Due Date","due Date"]))):
        due_date = i_sentence.translate({ord("|"): None}).split(" ")
        due_date = list(filter(None, due_date))

        dict_val.update({"Due Date":due_date[-1] })

      if (any(map(lambda word: word in i_sentence, ["Past Due","past Due"]))):
        past_due = i_sentence.translate({ord("|"): None}).split(" ")
        past_due = list(filter(None, past_due))

        dict_val.update({"Past Due":past_due[-1]})

      if (any(map(lambda word: word in i_sentence, ["New Charges"]))):
        new_charges = i_sentence.translate({ord("|"): None}).split(" ")
        new_charges = list(filter(None, new_charges))

        dict_val.update({"New Charges":new_charges[-1]  })

      if (any(map(lambda word: word in i_sentence, ["Total Amount Due"]))):
        total_amount = i_sentence.translate({ord("|"): None}).split(" ")
        total_amount = list(filter(None, total_amount)) 

        dict_val.update({"Total Amount":total_amount[-1] })

  if(loc["id"]=="details"):
    data_list = text.split('\n')
    name = " ".join(data_list[0].split(" ")[1:])
    mailing_address = " ".join(data_list[1].split(" ")[1:]) +" / "+" ".join(data_list[2].split(" ")[1:])
    service_address = " ".join(data_list[3].split(" ")[1:]) + " / "+" ".join( data_list[4].split(" ")[1:]   )

    dict_val.update({ "Name":name , "Mailing Address":mailing_address , "Service Address":service_address})


  if(loc["id"]=="amount"):
    data_list = text.split("\n")[:-1]

    for i_sentence in data_list :

      if (any(map(lambda word: word in i_sentence, ["TOTAL AMOUNT DUE","AMOUNT DUE"]))):
        total_amount_due = i_sentence.split(" ")[-1]

        dict_val.update({"Total Amount Due":total_amount_due})

      if (any(map(lambda word: word in i_sentence, ["PREVIOUS BALANCE","PREVIOUS","BALANCE"]))):
        previous_balance = i_sentence.split(" ")[-1]

        dict_val.update({"Previous Balance":previous_balance})

      if (any(map(lambda word: word in i_sentence, ["PAYMENTS"]))):
        payments = i_sentence.split(" ")[-1]

        dict_val.update({"Payments":payments})

      if (any(map(lambda word: word in i_sentence, ["TOTAL NEW CHARGES"]))):
        total_new_charges = i_sentence.split(" ")[-1]

        dict_val.update({"Total New Charges":total_new_charges})

      if (all(map(lambda word: word not in i_sentence, ["TOTAL AMOUNT DUE","AMOUNT DUE" ,"PREVIOUS BALANCE","PREVIOUS","BALANCE","NEW CHARGES" ,"PAYMENTS" , "TOTAL NEW CHARGES" ]))):
        bill_name = " ".join(i_sentence.split(" ")[:-1])
        bill_name_date = i_sentence.split(" ")[-1]
        if(bill_name != ""):
          dict_val.update({bill_name : bill_name_date})


  if(loc["id"]=="account number"):
    data_list =text.split("\n")[:-1]
    account_number = data_list[-1]
    
    dict_val.update({"Account Number":account_number})

  if(loc["id"] =="parcel"):
    data_list = text.split("\n")[:-1]
    parcel_number = data_list[-1]

    dict_val.update({"Parcel":parcel_number})

  if(loc["id"]=="meter_readings"):
    data_list = text.split("\n")[2:-1]
    if (any(map(lambda word: word in text , ["Meter Readings","Meter No","Previous","CUrrent"]))):
      for i , i_sentence in enumerate(data_list) :
        if (any(map(lambda word: word not in i_sentence, ["+Meter qualifies for smart irrigation rate","+Meter","qualifies for smart irrigation"]))):

          i_data = i_sentence.split(" ")[:9]
          meter_no = i_data[0]
          readings= i_data[1:-2]
          date_1 = None
          date_1_read= None
          date_2 = None
          date_2_read= None
          if(len(readings)==6 ):
            date_1 = " ".join(i_data[1:3])
            date_1_read = i_data[3:4][0]
            date_2 = " ".join(i_data[4:6])
            date_2_read = i_data[6:7][0]

          if(len(readings)==5 ):
            date_1 = " ".join(i_data[1:3])
            date_1_read = i_data[3:4][0]
            date_2 = " ".join(i_data[4:5])
            date_2_read = i_data[5:6][0]

          elif(len(readings)==4):
            date_1 = i_data[1]
            date_1_read = i_data[2]
            date_2 = i_data[3]
            date_2_read = i_data[4]

          dict_val.update({"Meter {}".format(i+1):meter_no , "Preivous Date {}".format(i+1):date_1,
                          "Previous Read {}".format(i+1):date_1_read , "Current Date {}".format(i+1):date_2 ,
                          "Current Read {}".format(i+1):date_2_read} )
        

    
  return dict_val