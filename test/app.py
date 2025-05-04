from flask import Flask, render_template, request
import convertdate

app = Flask(__name__)

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

def tinh_can_chi_nam(nam_am):
    can = CAN[nam_am % 10]
    chi = CHI[nam_am % 12]
    return f"{can} {chi}"

def tinh_quai_menh(nam_am, gioi_tinh):
    tong = sum(int(ch) for ch in str(nam_am))
    so_du = tong % 9
    if so_du == 0:
        so_du = 9

    bang_nam = {
        1: "KHẢM", 2: "LY", 3: "CẤN", 4: "ĐOÀI", 5: "CÀN",
        6: "KHÔN", 7: "TỐN", 8: "CHẤN", 9: "KHÔN", 0: "KHÔN"
    }

    bang_nu = {
        1: "CẤN", 2: "CÀN", 3: "ĐOÀI", 4: "CẤN", 5: "LY",
        6: "KHẢM", 7: "KHÔN", 8: "CHẤN", 9: "TỐN", 0: "TỐN"
    }

    if gioi_tinh.lower() == 'nam':
        return bang_nam.get(so_du)
    else:
        return bang_nu.get(so_du)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            ngay = int(request.form['ngay'])
            thang = int(request.form['thang'])
            nam = int(request.form['nam'])
            gioi_tinh = request.form['gioi_tinh']
            loai_lich = request.form['loai_lich']

            if loai_lich == "duong":
                am = convertdate.lunardate.from_gregorian(nam, thang, ngay)
                nam_am = am[0]
                ngay_duong = f"{ngay:02d}/{thang:02d}/{nam}"
                ngay_am = f"{am[2]:02d}/{am[1]:02d}/{am[0]}"
            else:
                nam_am = nam
                ngay_am = f"{ngay:02d}/{thang:02d}/{nam}"
                am = convertdate.lunardate.to_gregorian(nam, thang, ngay)
                ngay_duong = f"{am[2]:02d}/{am[1]:02d}/{am[0]}"

            can_chi = tinh_can_chi_nam(nam_am)
            quai = tinh_quai_menh(nam_am, gioi_tinh)

            return render_template('result.html', ngay_duong=ngay_duong, ngay_am=ngay_am, quai=quai, can_chi=can_chi)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
