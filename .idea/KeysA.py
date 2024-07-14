import psycopg2
import pandas as pd

def get_top10_debtors(db_uri, table_name):
    try:
        conn = psycopg2.connect(db_uri)
        cursor = conn.cursor()

        query = f"""
        SELECT "DebtorName", COUNT(*) as ObligationCount
        FROM public."{table_name}"
        GROUP BY "DebtorName"
        ORDER BY ObligationCount DESC
        LIMIT 10;
        """

        cursor.execute(query)
        results = cursor.fetchall()

    except Exception as e:
        print(f"Ошибка при подключении к базе данных или выполнении запроса: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    df = pd.DataFrame(results, columns=['DebtorName', 'ObligationCount'])

    print("10 лиц с наибольшим количеством обязательств:")
    print(top_debtors)

