import psycopg2
import pandas as pd


def get_top10_debtors(db_uri):
    table_name = 'MonetaryObligation'
    try:
        conn = psycopg2.connect(db_uri)
        cursor = conn.cursor()

        query = f"""
        SELECT "DebtorName", "DebtorInn", COUNT(*) as ObligationCount
        FROM public."{table_name}"
        GROUP BY "DebtorName", "DebtorInn"
        ORDER BY ObligationCount DESC
        LIMIT 10;
        """

        cursor.execute(query)
        results = cursor.fetchall()

    except Exception as e:
        print(f"Что-то пошло не так: {e}")
    finally:
        df = pd.DataFrame(results, columns=['DebtorName', 'DebtorInn', 'ObligationCount'])
        df.index += 1
        print("10 лиц с наибольшим количеством обязательств:")
        print(df)
        if cursor:
            cursor.close()
        if conn:
            conn.close()





