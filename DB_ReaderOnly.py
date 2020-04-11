
class DB_Reader:
    import pymysql
    pyConnector = pymysql.connect(
        host='localhost',
        user='root',
        passwd='DasWort9',
        database='quotesscraper'
    )
    

    def __init__(self):
        with self.pyConnector as cursor:
            cursor.execute("USE quotesscraper;")
            self.pyConnector.commit()

    def exec_n_fetchall(self, sql_cmd):
        '''
        Accepts connection object and SQL
        returns "fetchall" as result
        '''
        if not sql_cmd:
            raise ValueError('All arguments must contain values')
            return None

        with self.pyConnector as cursor:
            cursor.execute(sql_cmd)
            return cursor.fetchall()

    def catch(self):
        """
        Connects to localhost MySQL DB, root user.
        Fetches all available quotes and randomly chooses one.
        Gets author's description
        Returns dict with keys: [quote,tags,author,a_initials,a_country,a_bdate,a_bio]
        """
        from random import choice
        result1 = choice(self.exec_n_fetchall("SELECT * FROM quotes;"))[1:-1]
        result2 = self.exec_n_fetchall(f"SELECT * FROM authors WHERE author ='{result1[1]}';")[0][2:]

        str_quote = result1[0]
        str_author = result1[1]
        str_initials= f"{result1[1].split(' ')[0][0]}. {result1[1].split(' ')[-1][0]}."
        str_tags = result1[2].replace("_"," ")
        str_country =result2[0]
        str_bdate = result2[1]
        str_bio = result2[2]

        return dict(
            quote=str_quote,
            tags = str_tags,
            author = str_author,
            a_initials = str_initials,
            a_country = str_country,
            a_bdate = str_bdate,
            a_bio = str_bio
        )