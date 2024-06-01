from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kalkulator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            color: #333;
            margin: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .calculator {
            background-color: #ffffff;
            color: #333;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 20px;
        }
        h2 {
            margin-bottom: 20px;
            color: #4CAF50;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }
        input {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: calc(100% - 22px);
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            background-color: #4CAF50;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            text-align: left;
        }
        .result pre {
            background: #f9f9f9;
            color: #333;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        @media screen and (max-width: 600px) {
            .calculator {
                width: calc(100% - 40px);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="calculator">
            <h2>Kalkulator Permutasi</h2>
            <form action="/hitung_permutasi" method="post">
                <label for="n">Jumlah elemen (n):</label>
                <input type="number" id="n" name="n" required>
                <label for="r">Elemen yang diambil (r):</label>
                <input type="number" id="r" name="r" required>
                <button type="submit">Hitung Permutasi</button>
            </form>
            <div class="result">
                {% if permutation_result %}
                    <h3>Hasil Permutasi:</h3>
                    <pre>{{ permutation_result }}</pre>
                {% endif %}
            </div>
        </div>
        <div class="calculator">
            <h2>Kalkulator Faktorial</h2>
            <form action="/hitung_faktorial" method="post">
                <label for="number">Masukkan sebuah bilangan:</label>
                <input type="number" id="number" name="number" required>
                <button type="submit">Hitung Faktorial</button>
            </form>
            <div class="result">
                {% if factorial_result %}
                    <h3>Hasil Faktorial:</h3>
                    <pre>{{ factorial_result }}</pre>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

def hitung_faktorial(n):
    if n == 0:
        return "1"
    else:
        hasil = 1
        langkah = 1
        steps = []
        while n > 1:
            hasil *= n
            steps.append(f"{langkah}. {n} x {hasil // n} = {hasil}")
            n -= 1
            langkah += 1
        return "\n".join(steps)

def permutasi(n, r):
    if r > n:
        return 0
    if r == 0:
        return 1
    hasil = 1
    langkah = 1
    steps = []
    while r > 0:
        steps.append(f"{langkah}. {n} x {hasil} / {r} = {n * hasil // r}")
        hasil *= n
        n -= 1
        r -= 1
        langkah += 1
    return hasil, "\n".join(steps)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/hitung_faktorial', methods=['POST'])
def hitung_faktorial_route():
    try:
        number = int(request.form['number'])
        if number < 0:
            factorial_result = "Bilangan harus positif."
        else:
            factorial_result = hitung_faktorial(number)
    except ValueError:
        factorial_result = "Input harus berupa bilangan bulat."
    return render_template_string(HTML_TEMPLATE, factorial_result=factorial_result)

@app.route('/hitung_permutasi', methods=['POST'])
def hitung_permutasi_route():
    try:
        n = int(request.form['n'])
        r = int(request.form['r'])
        if r > n:
            permutation_result = "Elemen yang diambil (r) tidak boleh lebih besar dari jumlah elemen (n)."
        else:
            hasil_permutasi, langkah_permutasi = permutasi(n, r)
            permutation_result = f"Hasil Permutasi: {hasil_permutasi}\nLangkah-langkah:\n{langkah_permutasi}"
    except ValueError:
        permutation_result = "Input harus berupa bilangan bulat."
    return render_template_string(HTML_TEMPLATE, permutation_result=permutation_result)

if __name__ == '__main__':
    app.run(debug=True)
