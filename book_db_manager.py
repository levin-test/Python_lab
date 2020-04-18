import sqlite3

NAME_COL_NUM = 0


def start():
    while True:
        print("Main Menu")
        print("全件表示:1 新規作成:2 検索:3 ")
        mode_num = input("Please Select a Mode => ")
        if mode_num == "1":
            show_all()
            print()
        elif mode_num == "2":
            create_data()
            print()
        elif mode_num == "3":
            search_data()
            print()
        else:
            break

    print("Bye!")


def initializer():
    dbname = "MyBooks.sqlite"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(
        """
        create table books(
        isbn integer primary key , name text, purchase_price integer,
        retail_price integer, media text, shop_id text, finished_read boolean);
        """
    )

    conn.close()


def create_data():
    dbname = "MyBooks.sqlite"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    print("データを新規作成します。")
    book_name = input("Book Name: ")
    purchase_price = int(input("Purchase Price: "))
    retail_price = int(input("Retail Price: "))
    media = input("Media: ")
    isbn = input("ISBN: ")
    shop_id = input("Shop ID: ")
    # finished_read = input("Have you already read this book?")

    c.execute(
        """
        insert into books (isbn, name, purchase_price, retail_price,
         media, shop_id, finished_read)
         values(?, ?, ?, ?, ?, ?, ?);
        """,
        (isbn, book_name, purchase_price, retail_price, media, shop_id, True),
    )
    conn.commit()
    conn.close()


def search_data():
    dbname = "MyBooks.sqlite"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    def search_with_isbn():
        search_num = input("Input the isbn")
        c.execute(
            """
            select * from books where isbn = ?;
            """,
            # 第２引数は必ずタプルにする。
            (search_num,),
        )
        match_item = c.fetchone()
        conn.close()
        return match_item

    def search_with_name():
        print("2 Mode!")
        return None

    print("Search Mode!")
    mode_num = input("ISBNで探す:1  書名で探す:2")
    if mode_num == "1":
        print(search_with_isbn())
    elif mode_num == "2":
        search_with_name()
        return None
    else:
        print("入力が間違っています。")
        return None


def show_all():
    dbname = "MyBooks.sqlite"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(
        """
        select name from books;
        """
    )
    print('====================')
    for item in c.fetchall():
        print(item[NAME_COL_NUM])
        print('====================')
    conn.close()
    return


if __name__ == "__main__":
    start()
