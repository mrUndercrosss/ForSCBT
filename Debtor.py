import pandas as pd
from sqlalchemy import create_engine


def write_info_debtor(data, db_uri):
    table_name = 'Debtor'
    debtor_info_list = []

    for entry in data:
        debtor_info = {}
        keys_to_add = ['MessageId', 'DebtorName', 'DebtorInn', 'DebtorBirthDate', 'DebtorBirthPlace',
                       'DebtorAddress', 'PublisherName', 'PublisherInn', 'PublisherOgrn',
                       'DebtorSnils', 'PreviousName']
        debtor_info.update((key, entry[key]) for key in keys_to_add if key in entry)
        name_history = entry.get('NameHistory', [])
        debtor_info['NameHistory'] = ', '.join(name_history) if name_history else None
        debtor_info_list.append(debtor_info)

    df = pd.DataFrame(debtor_info_list)
    engine = create_engine(db_uri)
    with engine.connect() as connection:
        df.to_sql(table_name, con=connection, if_exists='replace', index=False)



