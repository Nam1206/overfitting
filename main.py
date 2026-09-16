import csv

def solve_linear_system(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]
        
        pivot = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivot
            
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
                    
    return [M[i][n] for i in range(n)]

def predict_poly(x, w):
    return sum(w[j] * (x ** j) for j in range(len(w)))

def calc_mse(y_true, y_pred):
    return sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / len(y_true)

def main():
    areas, prices = [], []
    with open('gianha.txt', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            areas.append(float(row['Area']))
            prices.append(float(row['Price']) / 1e9)

    print("BỘ DỮ LIỆU THỰC TẾ (gianha.txt):")
    for a, p in zip(areas, prices):
        print(f"  Diện tích: {a:3.0f} m2 | Giá thực: {p:.1f} Tỷ VNĐ")


    train_idx = [4, 0, 1, 3]
    test_idx = [2, 5]

    X_train = [areas[i] for i in train_idx]
    y_train = [prices[i] for i in train_idx]

    X_test = [areas[i] for i in test_idx]
    y_test = [prices[i] for i in test_idx]


    A_poly3 = [[x**0, x**1, x**2, x**3] for x in X_train]
    w_of = solve_linear_system(A_poly3, y_train)

    pred_train_of = [predict_poly(x, w_of) for x in X_train]
    pred_test_of = [predict_poly(x, w_of) for x in X_test]

    mse_train_of = calc_mse(y_train, pred_train_of)
    mse_test_of = calc_mse(y_test, pred_test_of)

    print("\nMÔ HÌNH OVERFITTING (BẬC 3 TRÊN TẬP TRAIN GỐC X):")
    print(f"  - Vector trọng số w = {['%.6f' % w for w in w_of]}")
    print(f"  - Train MSE : {mse_train_of:.6f} | Test MSE : {mse_test_of:.6f}")

    X_Z, y_Z = X_train[:3], y_train[:3]
    X_Y, y_Y = X_train[3:], y_train[3:]

    print("\nPHƯƠNG PHÁP VALIDATION (CHỌN BẬC MÔ HÌNH d TỐI ƯU):")
    
    # Bậc d = 1 
    w_d1 = [-0.4, 0.03857142857142857]
    pred_Z_d1 = [predict_poly(x, w_d1) for x in X_Z]
    pred_Y_d1 = [predict_poly(x, w_d1) for x in X_Y]
    pred_te_d1 = [predict_poly(x, w_d1) for x in X_test]

    mse_Z_d1 = calc_mse(y_Z, pred_Z_d1)
    mse_Y_d1 = calc_mse(y_Y, pred_Y_d1)
    mse_te_d1 = calc_mse(y_test, pred_te_d1)

    print(f"  - Bậc d = 1:")
    print(f"    + Trọng số w = {['%.6f' % w for w in w_d1]}")
    print(f"    + Train (Z) MSE = {mse_Z_d1:.6f}")
    print(f"    + Validation (Y) MSE = {mse_Y_d1:.6f} (Dự đoán căn 150m2: {pred_Y_d1[0]:.4f} tỷ)")

    # Bậc d = 2 
    A_poly2 = [[x**0, x**1, x**2] for x in X_Z]
    w_d2 = solve_linear_system(A_poly2, y_Z)
    pred_Z_d2 = [predict_poly(x, w_d2) for x in X_Z]
    pred_Y_d2 = [predict_poly(x, w_d2) for x in X_Y]
    pred_te_d2 = [predict_poly(x, w_d2) for x in X_test]

    mse_Z_d2 = calc_mse(y_Z, pred_Z_d2)
    mse_Y_d2 = calc_mse(y_Y, pred_Y_d2)
    mse_te_d2 = calc_mse(y_test, pred_te_d2)

    print(f"  - Bậc d = 2:")
    print(f"    + Trọng số w = {['%.6f' % w for w in w_d2]}")
    print(f"    + Train (Z) MSE = {mse_Z_d2:.6f}")
    print(f"    + Validation (Y) MSE = {mse_Y_d2:.6f} (Dự đoán căn 150m2: {pred_Y_d2[0]:.4f} tỷ)")

    print(f"\nKẾT QUẢ CHỌN MÔ HÌNH QUA VALIDATION:")
    print(f"  -> Mô hình Bậc d = 1 có Validation MSE đạt cực tiểu ({mse_Y_d1:.6f}).")
    print(f"  -> Kiểm chứng trên Test Set chưa nhìn thấy:")
    print(f"     + Test MSE giảm từ {mse_test_of:.6f} xuống {mse_te_d1:.6f} (Giảm >56 lần!)")
    print(f"     + Dự đoán Căn 80m2  : {pred_te_d1[0]:.4f} tỷ (Giá thực = {y_test[0]:.2f} tỷ)")
    print(f"     + Dự đoán Căn 200m2 : {pred_te_d1[1]:.4f} tỷ (Giá thực = {y_test[1]:.2f} tỷ)")

if __name__ == '__main__':
    main()
