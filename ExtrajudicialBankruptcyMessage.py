import pandas as pd
from sqlalchemy import create_engine


def write_info_message(data, db_uri):
    table_name = 'ExtrajudicialBankruptcyMessage'
    message_info_list = []

    for entry in data:
        message_info = {}
        keys_to_add = ['MessageId', 'DebtorName', 'DebtorInn', 'Number', 'MessageType', 'PublishDate', 'FinishReason']
        message_info.update((key, entry[key]) for key in keys_to_add if key in entry)
        message_info_list.append(message_info)

    df = pd.DataFrame(message_info_list)
    engine = create_engine(db_uri)
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='replace', index=False)

