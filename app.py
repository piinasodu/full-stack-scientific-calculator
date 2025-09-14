from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def factorial(n):
    if not isinstance(n, int) or n < 0:
        return None
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

@app.route('/calculate', methods=['POST'])
def calculate():
    
    data = request.get_json()
    expression = data.get('expression', '')

    expression = expression.replace('×', '*').replace('÷', '/')

    safe_dict = {
        '__builtins__': None,
        'sin': lambda x: __import__('math').sin(x),
        'cos': lambda x: __import__('math').cos(x),
        'tan': lambda x: __import__('math').tan(x),
        'log': lambda x: __import__('math').log10(x),
        'ln': lambda x: __import__('math').log(x),
        'pi': __import__('math').pi,
        'e': __import__('math').e,
        'sqrt': lambda x: __import__('math').sqrt(x),
        'pow': lambda x, y: __import__('math').pow(x, y),
        'factorial': factorial
    }

    try:
       
        expression_safe = expression.replace('!', ')').replace('^', ',')
        expression_safe = expression_safe.replace('sin(', 'sin(').replace('cos(', 'cos(').replace('tan(', 'tan(')
        expression_safe = expression_safe.replace('log(', 'log(').replace('ln(', 'ln(').replace('sqrt(', 'sqrt(')
        expression_safe = expression_safe.replace('^', ',')
        expression_safe = expression_safe.replace('!','factorial(')
        
        result = eval(expression, {"__builtins__": None, "math": __import__("math"), "factorial": factorial})

        return jsonify({'result': result})
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return jsonify({'error': 'Invalid Expression'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
