from datetime import date, datetime, timedelta
import pickle


DATA_FILE = "./TaskCalDB.pickle"
PROJECT_LIST = "Project List"
route_dict = {}


def app():
    load_from_binary()
    while True:
        print("追加:1, 削除:2, 一覧表示:3, 登録PJリスト:4, 初期化:5, 終了:e")
        mode_num = input("モードを選択 => ")
        if mode_num == "1":
            add_mode()
        elif mode_num == "2":
            del_mode()
        elif mode_num == "3":
            show_summary()
        elif mode_num == "4":
            show_project_list()
        elif mode_num == "5":
            initializer()
        elif mode_num == "e":
            print("終了しました。")
            save_into_binary(route_dict)
            break
        else:
            print("不正な入力です。")
        print()
    return None


# 汎用関数
# 開始日と終了日の間のdatetimeオブジェクトを全て返す
def date_range(start_date: date, end_date: date):
    diff = (end_date - start_date).days + 1
    return (start_date + timedelta(i) for i in range(diff))


# 追加モード
def add_mode():
    name = input("プロジェクト名: ")
    start = input("開始予定日: ")
    end = input("終了予定日: ")
    unit = float(input("負荷単位: "))
    add_project_info(
        name,
        datetime.strptime(start, "%Y-%m-%d"),
        datetime.strptime(end, "%Y-%m-%d"),
        unit,
    )
    return None


# 削除モード
def del_mode():
    pj_name = input("削除するプロジェクト名を入力してください。")
    for k, v_list in route_dict.items():
        if k == PROJECT_LIST:
            continue
        for d in v_list:
            if d["project_name"] == pj_name:
                v_list.remove(d)
    route_dict[PROJECT_LIST].remove(pj_name)
    return None


# 登録プロジェクト全件表示
def show_project_list():
    for i in route_dict[PROJECT_LIST]:
        print(i)


# データ初期化
def initializer():
    result = date_range(
        start_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
        end_date=datetime.strptime("2020-12-31", "%Y-%m-%d"),
    )
    for i in result:
        ins_key_to_dict(i.strftime("%Y-%m-%d"))
    ins_key_to_dict(PROJECT_LIST)


# 辞書へ日程の格納処理
def ins_key_to_dict(ins_date: str):
    route_dict[ins_date] = []
    return None


# バイナリデータへの保存
def save_into_binary(dict_data: dict):
    with open(DATA_FILE, mode="wb") as f:
        pickle.dump(dict_data, f)
    return None


# バイナリデータからのロード
def load_from_binary():
    with open(DATA_FILE, mode="rb") as f:
        global route_dict
        route_dict = pickle.load(f)
    return None


# プロジェクト情報の追加
def add_project_info(pj_name: str, start_date: date, end_date: date, load_unit: float):
    project_info = {
        "project_name": pj_name,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "load_unit": load_unit,
    }

    route_dict[PROJECT_LIST].append(pj_name)

    for target_date in date_range(start_date=start_date, end_date=end_date):
        if target_date.strftime("%Y-%m-%d") in route_dict:
            route_dict[target_date.strftime("%Y-%m-%d")].append(project_info)
        else:
            route_dict[target_date.strftime("%Y-%m-%d")] = []
            route_dict[target_date.strftime("%Y-%m-%d")].append(project_info)
    return None


# 日付と負荷単位の一覧を表示
def show_summary():
    for k, v_list in route_dict.items():
        if k == PROJECT_LIST:
            continue
        load_unit_sum = 0
        pj_list = []
        for d in v_list:
            load_unit_sum += d["load_unit"]
            pj_list.append(d["project_name"])
        print("{}: {} {}".format(k, str(load_unit_sum).rjust(4, " "), pj_list))
    return None


if __name__ == "__main__":
    app()
