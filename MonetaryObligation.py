import pandas as pd
from sqlalchemy import create_engine


def write_info_monetary_obligation(data, db_uri):
    table_name = 'MonetaryObligation'
    monetary_obligation_list = []

    for entry in data:
        message_id = entry['MessageId']
        debtor_name = entry['DebtorName']
        debtor_inn = entry['DebtorInn']

        for obligation in entry['Obligations']:
            creditor_name = obligation['CreditorName']
            content = obligation['Content']
            basis = obligation['Basis']
            total_sum = obligation['TotalSum']
            debt_sum = obligation['DebtSum']
            penalty_sum = obligation['PenaltySum']

            monetary_obligation_list.append({
                'MessageId': message_id,
                'DebtorName': debtor_name,
                'DebtorInn': debtor_inn,
                'CreditorName': creditor_name,
                'Content': content,
                'Basis': basis,
                'TotalSum': total_sum,
                'DebtSum': debt_sum,
                'PenaltySum': penalty_sum
            })

    df = pd.DataFrame(monetary_obligation_list)
    engine = create_engine(db_uri)
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='replace', index=False)
