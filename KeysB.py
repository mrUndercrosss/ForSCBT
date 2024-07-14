import psycopg2
import pandas as pd


def get_top10_debtors_by_total_sum(db_uri):
    table_name = 'MonetaryObligation'
    try:
        conn = psycopg2.connect(db_uri)
        cursor = conn.cursor()

        query = f"""
        SELECT "DebtorName", "DebtorInn", SUM("TotalSum"::numeric) as TotalDebt
        FROM public."{table_name}"
        GROUP BY "DebtorName", "DebtorInn"
        ORDER BY TotalDebt DESC
        LIMIT 10;
        """

        cursor.execute(query)
        results = cursor.fetchall()

    except Exception as e:
        print(f"Что-то пошло не так: {e}")
    finally:
        df = pd.DataFrame(results, columns=['DebtorName', 'DebtorInn', 'TotalDebt'])
        df.index += 1
        print("10 лиц с наибольшей общей суммой задолженностей:")
        print(df)

        if cursor:
            cursor.close()
        if conn:
            conn.close()




