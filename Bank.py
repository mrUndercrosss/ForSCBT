import pandas as pd
from sqlalchemy import create_engine


def write_info_bank(data, db_uri):
    table_name = 'Bank'
    bank_list = []

    for entry in data:
        message_id = entry['MessageId']
        debtor_name = entry['DebtorName']
        debtor_inn = entry['DebtorInn']

        for obligation in entry['Bank']:
            bank_name = obligation['BankName']
            bik = obligation['BIK']

            bank_list.append({
                'MessageId': message_id,
                'DebtorName': debtor_name,
                'DebtorInn': debtor_inn,
                'BankName': bank_name,
                'BIK': bik,
            })

    df = pd.DataFrame(bank_list)
    engine = create_engine(db_uri)
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='replace', index=False)

