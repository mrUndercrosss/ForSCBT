import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import matplotlib.pyplot as plt


def calculate_age(birthdate_str):
    """Функция для расчета возраста"""
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%dT%H:%M:%SZ')
    today = datetime(2024, 1, 1)
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def to_float(value):
    """Так надо"""
    try:
        return float(value)
    except ValueError:
        return None


def plot_total_debt_by_age_category(db_uri):
    """Функция для построения графика с суммарной задолженностью по возрастным категориям"""
    engine = create_engine(db_uri)

    with engine.connect() as connection:
        debtor_df = pd.read_sql('SELECT "DebtorName", "DebtorBirthDate" FROM public."Debtor"', con=connection)
        debtor_df['Age'] = debtor_df['DebtorBirthDate'].apply(calculate_age)
        monetary_obligation_df = pd.read_sql('SELECT "DebtorName", "TotalSum" FROM public."MonetaryObligation"', con=connection)

    monetary_obligation_df['TotalSum'] = monetary_obligation_df['TotalSum'].apply(to_float)
    monetary_obligation_df = monetary_obligation_df.dropna(subset=['TotalSum'])
    grouped_obligations = monetary_obligation_df.groupby('DebtorName')['TotalSum'].sum().reset_index()
    merged_df = pd.merge(debtor_df, grouped_obligations, on='DebtorName', how='left')

    bins = range(0, 101, 10)
    labels = [f'{i}-{i+9}' for i in bins[:-1]]
    merged_df['AgeCategory'] = pd.cut(merged_df['Age'], bins=bins, labels=labels, right=False)

    age_grouped_df = merged_df.groupby('AgeCategory')['TotalSum'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(age_grouped_df['AgeCategory'], age_grouped_df['TotalSum'], color='skyblue')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 100000, round(yval, 2), ha='center', va='bottom')

    plt.xlabel('Возрастные категории, год')
    plt.ylabel('Суммарная задолженность, млн')
    plt.title('Суммарная задолженность различных возрастных категорий')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Настройка оси y
    plt.ylim(0, max(age_grouped_df['TotalSum']) + 200000)
    plt.yticks(range(0, int(max(age_grouped_df['TotalSum'])) + 200000, 100000))

    plt.show()
