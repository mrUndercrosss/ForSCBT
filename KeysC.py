import psycopg2
import pandas as pd


def get_debtors_payment_percentage(db_uri):
    try:
        conn = psycopg2.connect(db_uri)
        cursor = conn.cursor()

        # Рассчитываем общую сумму задолженностей для каждого физ лица
        total_debts_query = """
        SELECT "DebtorInn", SUM(CAST("TotalSum" AS numeric)) as TotalDebt
        FROM public."MonetaryObligation"
        GROUP BY "DebtorInn"
        """

        cursor.execute(total_debts_query)
        total_debts_results = cursor.fetchall()

        total_debts_df = pd.DataFrame(total_debts_results, columns=['DebtorInn', 'TotalDebt'])

        # Рассчитываем общую выплаченную сумму для каждого физ лица
        total_paid_query = """
        SELECT "DebtorInn", SUM(CAST("DebtSum" AS numeric) + CAST("PenaltySum" AS numeric)) as TotalPaid
        FROM public."MonetaryObligation"
        GROUP BY "DebtorInn"
        """

        cursor.execute(total_paid_query)
        total_paid_results = cursor.fetchall()

        total_paid_df = pd.DataFrame(total_paid_results, columns=['DebtorInn', 'TotalPaid'])
        combined_df = pd.merge(total_debts_df, total_paid_df, on='DebtorInn', how='outer')
        combined_df['PaymentPercentage'] = (combined_df['TotalPaid'] / combined_df['TotalDebt']) * 100
        sorted_df = combined_df.sort_values(by='PaymentPercentage').reset_index(drop=True)

    except Exception as e:
        print(f"Что-то пошло не так: {e}")
        sorted_df = pd.DataFrame()

    finally:
        df = pd.DataFrame(sorted_df, columns=['DebtorInn', 'TotalDebt', 'TotalPaid', 'PaymentPercentage'])
        df.index += 1
        print("Физические лица с процентом общей выплаченной суммы относительно общей суммы задолженностей (от меньшего к большему):")
        print(df)

        if cursor:
            cursor.close()
        if conn:
            conn.close()


