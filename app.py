from flask import Flask, request, jsonify

app =   Flask(__name__)


@app.route('/srechallenge', methods=['GET'])
def get_response():
    try:
        # Request customer query in url Example: http://localhost:5000/srechalenge?saludation=Hi
        saludation = request.args.get('saludation')
        # If saludation in URL is equal to Hi, Dear Sir or Madam or Moin it returns a customised message and status code 200.
        if saludation == "Hi": 
            data={"data":"Hi there!"}
            resp = jsonify(data)
            resp.status_code = 200
            return resp
        if saludation == "Dear Sir or Madam": 
            data={"data":"Yours faithfully"}
            resp = jsonify(data)
            resp.status_code = 200
            return resp
        if saludation == "Moin": 
            data={"data":"Moin moin!"}
            resp = jsonify(data)
            resp.status_code = 200
            return resp
        # If saludation is not the correct one show error message with status code 500
        else:
            data={"data":'Customer saludation {} not found.'.format(saludation)}
            resp = jsonify(data)
            resp.status_code = 500
            return resp
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=False, port=5000)
