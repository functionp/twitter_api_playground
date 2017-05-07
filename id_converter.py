from twitter_toolkit import *

# スクリーンネームファイルを読み込み
screen_name_file_path = "screen_names.txt"
screen_name_file = open(screen_name_file_path, "r")

# スクリーンネームファイルを一行づつ見て改行を除去し、スクリーンネームのリストを作る
screen_name_list = []
for line in screen_name_file.readlines():
    screen_name_list.append(line.replace("\n", ""))

screen_name_file.close()

id_str_list = []

# APIを使って screen_nameをIDに変換
for screen_name in screen_name_list:
    getter = UserGetter(screen_name)
    result_json = getter.collect()

    # IDの末尾に改行をつける
    id_str_list.append(result_json['id_str'] + "\n")

# IDのファイルに書き込み
id_str_file_path = "id_str,txt"
id_str_file = open(id_str_file_path, "w")
id_str_file.writelines(id_str_list)
id_str_file.close()


