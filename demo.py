from flask import Flask, request


app = Flask(__name__)

@app.route('/test', methods=['POST'])
def upload_file():
    print(123123)
    print(111111)
    print("test success!!!")
    return 'test success!!!', 200




if __name__ == '__main__':
    app.run(debug=True)