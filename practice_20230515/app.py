from flask import Flask, request, jsonify, render_template

import poker as p
import series as s
import model
from test_controller import test_controller

app = Flask(__name__, static_url_path="/resource", static_folder="./my_resource") # static_folder指向其他目錄
# app = Flask(__name__, static_url_path="/static", static_folder="./static") # static_folder指向其他目錄
app.register_blueprint(test_controller, url_prefix="/controller_A")

@app.route("/") # 定義一網址，觸發函數
def hello_flask():
    return "<h1>hello_flask</h1>"

@app.route("/helloFlask")
def hello_Flask():
    return "<h1>hello_Flask</h1>"

@app.route("/helloFlask/Allen")
def hello_Flask_Allen():
    return "<h1>Hello Allen!</h1>"

@app.route("/helloFlask/Ted")
def hello_Flask_Ted():
    return "<h1>Hello Ted!</h1>"

@app.route("/helloFlask/Jack")
def hello_Flask_Jack():
    return "<h1>Hello Jack!</h1>"

@app.route("/greet/<name>")
def greet(name):
    return "Hello {}".format(name)

@app.route("/greet/<name>/<age>")
def greet_info(name, age):
    return "Hello {}, you are {} years old.".format(name, age)

@app.route("/greet/<name>")
def greet_template(name):
	return render_template("hello.html",
						   name=name)
	# name 左邊=模板的變數名稱，右邊=python內的變數名稱

@app.route("/two_sum/<x>/<y>")  # 接收進來的都是字串
def two_sum(x, y):
    return str(int(x) + int(y))
    # 若需進行相加，需先轉為整數
    # 因有限定輸出型別，故需再轉回字串

""""
提供他人使用時，可以標註清楚
[GET] /get_names/department_id:string/team_id:string
Response:
    [
        {
            "emp_name": "Allen",
            "emp_id": 13
        },
        {
            "emp_name": "Ted",
            "emp_id": 44
        },...
    ]
"""
# 嚴謹寫法
@app.route("/get_names/<string:department_id>/<int:team_id>")
def get_names(deparment_id: str, team_id: int) -> str:
    sql = """
        SELECT emp_name, emp_id FROM emp
        WHERE department_id = '{}'
        AND team_id = '{}';
    """
    return sql

# /hello_get?name=Allen&age=22
@app.route("/hello_get", methods=["GET"])
def hello_get():   # 不用接受任何參數
    name = request.args.get("name") # get為把argument內容拿出來
    age = request.args.get("age")
    output_html = """
    <html>
        <head>
            <title>Hello</title>
        <head>
        <body>
    """

    if name is None:
        output_html = "<h1>What's your name?</h1>"
    elif age is None:
        output_html = "<h1>Hello {}.</h1>".format(name)
    else:
        output_html = "<h1>Hello {}, you are {} years old.</h1>".format(name, age)

    return output_html

# /hello_get?name=Allen&age=22
@app.route("/hello_get_template")
def hello_get_template():
	name = request.args.get("name")
	age = request.args.get("age")

	return render_template(
		"hello_get.html",
		name=name,
		age=age,
	)

@app.route("/hello_post", methods=["GET", "POST"])
def hello_post():
    output_html = """
        <form action="/hello_post" method="POST">
            <label>What's your name?</label><br>
            <input name="username">
            <button type="submit">SUBMIT</button>
        </form>
    """

    request_method = request.method
    if request_method == "POST":
        username = request.form.get("username")
        output_html += "<h1>Hello {}.</h1>".format(username)

    return output_html

@app.route("/hello_post2", methods=["GET", "POST"])
def hello_post2():
	if request.method == 'GET':
			return render_template('hello_post.html')

	elif request.method == "POST":
			username = request.form.get("username")
			return render_template('hello_post.html',
								   username=username,
								   request_method='post')

# /series?n=11
@app.route('/series')
def series():
    n = int(request.args.get('n'))
    print(n)
    output = str(s.Func(n))
    print(output)
    return output

@app.route("/poker/<num>")
def poker_num(num):
	json_data = p.poker(int(num))

	return jsonify(json_data)

# /poker
@app.route('/poker', methods=['GET', 'POST'])
def poker():
		if request.method == 'GET':
			outStr: str = """
			<html>
				<head>
					<title>poker</title>
				</head>
				<body>
					<h1>How many players?</h1>
					<form action="/poker" method="post">
						<input type="textbox" name="players">
						<button type="submit">Submit</button>
					</form>
				</body>
			</html>
			"""
			return outStr
		elif request.method == 'POST':
			players = request.form.get('players')
			cards = p.poker(int(players))
			return jsonify(cards)   # 利用jsonify回傳json

@app.route('/poker2', methods=['GET', 'POST'])
def poker2():
		if request.method == 'GET':
			return render_template('poker.html')
		elif request.method == 'POST':
			player = request.form.get('player')
			cards = p.poker(int(player))
			return render_template('poker.html',
									player=player,
								    request_method='post')

@app.route('/show_staff')
def hello_google():
	staff_data = model.getStaff()
	column = ['ID', 'Name', 'DeptId', 'Age', 'Gender', 'Salary']
	return render_template('show_staff.html', staff_data=staff_data,
											  column=column)

if __name__ == "__main__":
	app.run(debug=True, host="localhost", port=5000)
	# app.run(debug=True, host="0.0.0.0", port=5000)
	# host用於限制哪台電腦可以訪問(類似防火牆)
	# 如果有更改內容，須重開伺服器，若加上debug則不用