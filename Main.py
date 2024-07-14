from Parsing import read_data
from KeysA import get_top10_debtors
from KeysB import get_top10_debtors_by_total_sum
from KeysC import get_debtors_payment_percentage
from Vizualize import plot_total_debt_by_age_category


def main(file_path, db_uri):
    read_data(file_path, db_uri)
    get_top10_debtors(db_uri)
    print()
    get_top10_debtors_by_total_sum(db_uri)
    print()
    get_debtors_payment_percentage(db_uri)
    plot_total_debt_by_age_category(db_uri)


if __name__ == "__main__":
    # Путь к файлу и коннект к бд
    xml_file_path = r'C:\Users\Konstantin\Desktop\SCBT\ExtrajudicialBankruptcy_20230808_2.xml'
    db_uri = 'postgresql://testuser:mr_undercross48162@localhost:5432/individuals'

    main(xml_file_path, db_uri)
