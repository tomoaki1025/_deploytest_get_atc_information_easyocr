from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
import csv
from get_info import get_metar_taf
from main import get_gai_comme

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class Info:
    info_dict = None


@app.route("/")
def home():
    list_of_info = get_gai_comme()
    list_of_info.update(get_metar_taf())
    Info.info_dict = list_of_info
    return render_template("index.html", info=list_of_info)


@app.route("/download", methods=['GET', 'POST'])
def download():
    with open('./atc_info.csv', 'w') as f:
        key_list = [key for key, value in Info.info_dict.items()]  # 下のfieldnamesへ
        writer = csv.DictWriter(f, fieldnames=[key for key in key_list], extrasaction='ignore')
        data = [Info.info_dict]
        writer.writeheader()
        writer.writerows(data)

    PATH = 'atc_info.csv'
    return send_file(PATH, as_attachment=True)


# @app.route('/cafes')
# def cafes():
#     with open('cafe-data.csv', encoding="utf-8", newline='') as csv_file:
#         csv_data = csv.reader(csv_file, delimiter=',')
#         list_of_rows = []
#         for row in csv_data:
#             list_of_rows.append(row)
#     return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)