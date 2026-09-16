# Phân Tích và Khắc Phục Overfitting Trong Hồi Quy Đa Thức

Dự án mô phỏng hiện tượng **Overfitting (Quá khớp)** trên bộ dữ liệu giá nhà thực tế (`gianha.txt`) và áp dụng **Phương pháp Validation** để tìm độ phức tạp mô hình tối ưu.

---

## 1. Dữ Liệu Đầu Vào (`gianha.txt`)

Bộ dữ liệu gồm 6 căn nhà với thông tin diện tích (`Area`) và giá thực tế (`Price`):
- **Tập Huấn luyện (Train gốc $X$)**: 4 căn ($60m^2$, $100m^2$, $120m^2$, $150m^2$)
- **Tập Kiểm thử (Test)**: 2 căn chưa nhìn thấy ($80m^2$ giá 2.6 tỷ, $200m^2$ giá 7.0 tỷ)

---

## 2. Nguyên Nhận Gây Overfitting (Ngắn Gọn)

1. **Lượng dữ liệu huấn luyện quá ít**: Tập train gốc chỉ có **4 điểm dữ liệu**.
2. **Mô hình quá phức tạp**: Đa thức bậc 3 ($d=3$) có 4 tham số ($w_0, w_1, w_2, w_3$), ép đường cong đi qua chính xác cả 4 điểm train.
3. **Hệ quả**: $\text{Train MSE} = 0.000000$ (khớp tuyệt đối) nhưng $\text{Test MSE}$ bùng nổ lên **$3.003457$**.

---

## 3. Giải Pháp Khắc Phục Bằng Phương Pháp Validation

Tách tập Train gốc $X$ thành 2 phần:
- **Tập Train mới ($Z$)**: 3 căn ($60m^2, 100m^2, 120m^2$)
- **Tập Validation ($Y$)**: 1 căn ($150m^2$, giá thực = 5.50 tỷ)

### Kết quả đánh giá Validation Error:
- **Bậc $d=1$**: $\text{Validation MSE} = \mathbf{0.013061}$ (**Đạt cực tiểu**)
- **Bậc $d=2$**: $\text{Validation MSE} = 0.140625$
- **Bậc $d=3$**: $\text{Validation MSE} = 0.436503$

👉 **Quyết định**: Chọn **Mô hình Bậc 1 ($d=1$)** theo quy tắc chọn điểm cực tiểu của Validation Error.

---

## 4. Kết Quả Kiểm Chứng Trên Tập Test

Khi áp dụng mô hình Bậc 1 ($\hat{y} = -0.4000 + 0.038571 \cdot x$):
- $\text{Test MSE}$ giảm từ **$3.003457$** xuống còn **$0.053061$** (Giảm >56 lần!).
- **Dự báo căn $80m^2$**: $2.6857$ tỷ (Giá thực $2.60$ tỷ)
- **Dự báo căn $200m^2$**: $7.3143$ tỷ (Giá thực $7.00$ tỷ)

---

## 5. Hướng Dẫn Chạy Code

```bash
python main.py
```
