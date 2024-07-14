import pandas as pd
from sqlalchemy import create_engine


def write_info_obligation_payment(data, db_uri):
    table_name = 'ObligationPayment'
    obligation_payment_list = []

    for entry in data:
        message_id = entry['MessageId']
        debtor_name = entry['DebtorName']
        debtor_inn = entry['DebtorInn']

        for obligation in entry['ObligationPayment']:
            obligation_payment_name = obligation['PaymentName']
            obligation_payment_sum = obligation['PaymentSum']
            obligation_payment_penalty_sum = obligation['Payment_penalty_sum']

            obligation_payment_list.append({
                'MessageId': message_id,
                'DebtorName': debtor_name,
                'DebtorInn': debtor_inn,
                'ObligationPaymentName': obligation_payment_name,
                'ObligationPaymentSum': obligation_payment_sum,
                'ObligationPaymentPenaltySum': obligation_payment_penalty_sum
            })

    df = pd.DataFrame(obligation_payment_list)
    engine = create_engine(db_uri)
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='replace', index=False)

