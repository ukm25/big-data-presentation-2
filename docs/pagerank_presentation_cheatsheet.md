# 🚀 Bí Kíp Thuyết Trình: Thuật Toán PageRank

Tài liệu này tổng hợp toàn bộ các điểm mấu chốt để bạn tự tin trình bày dự án PageRank trên Spark.

## 1. Ý tưởng cốt lõi: "Cuộc bầu cử uy tín"
- **Phiếu bầu:** Mỗi đường link từ trang A trỏ đến trang B là một "phiếu bầu" của A cho B.
- **Giá trị phiếu bầu:** Phiếu bầu từ một trang quan trọng (uy tín cao) có giá trị cực lớn so với phiếu bầu từ trang vô danh.
- **Tính sẻ chia:** Một trang có 1.0 điểm nhưng trỏ đến 5 trang khác thì mỗi trang đích chỉ nhận được 0.2 điểm.

## 2. Công thức "Vàng" của Google
$$PR(j) = 0.15 + 0.85 \times \sum_{i \in B_j} \frac{PR(i)}{L(i)}$$

- **Hệ số 0.85 (Hệ số cản):** Xác suất người dùng lướt web theo các link có sẵn. Ngăn chặn điểm số tăng vô hạn trong các vòng lặp kín.
- **Hệ số 0.15 (Nhảy ngẫu nhiên):** Đảm bảo mọi trang web đều có tối thiểu 0.15 điểm, không trang nào bị "biến mất".
- **Tính bảo toàn:** Tổng điểm của toàn bộ hệ thống luôn bằng đúng số lượng trang web ($N$). Nếu có 1 triệu trang, tổng PR luôn là 1 triệu.

## 3. Tại sao PageRank + Spark = Cực mạnh?
- **Tính lặp (Iterative):** PageRank cần chạy nhiều vòng (vòng 1, vòng 2...) để điểm số ổn định (hội tụ).
- **Caching:** Đồ thị liên kết (`links`) không đổi qua các vòng. Spark dùng hàm `.cache()` để giữ đồ thị này trên RAM, giúp tốc độ nhanh hơn MapReduce (vốn phải đọc/ghi đĩa cứng liên tục) gấp 10-100 lần.

## 4. Bảng tính mẫu (Ví dụ hội đồng yêu cầu tính tay)
*Giả sử 4 trang: A→(B,C); B→C; C→A; D→C.*

| Vòng | Trang A | Trang B | Trang C | Trang D | Ghi chú |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **0** | **1.000** | **1.000** | **1.000** | **1.000** | Khởi tạo |
| **1** | 1.000 | 0.575 | **2.275** | 0.150 | C dẫn đầu |
| **2** | **2.084** | 0.575 | 1.191 | 0.150 | A vọt lên nhờ C trả điểm |
| **10** | **1.500** | **0.780** | **1.570** | **0.150** | **HỘI TỤ** |

## 5. Trả lời các câu hỏi "Hóc búa"
- **H: Khi nào thuật toán dừng lại?**
  - Tr: Khi sự thay đổi điểm số giữa các vòng lặp nhỏ hơn một ngưỡng cho phép (Tolerance), hoặc sau một số vòng lặp cố định (như 10 vòng trong bài này).
- **H: "Hố đen" điểm số là gì (Sink nodes)?**
  - Tr: Là những trang web có link trỏ đến nhưng nó không trỏ đi đâu cả. Điểm số lọt vào đây sẽ bị mất, khiến tổng PR của hệ thống giảm dần. 
- **H: Vì sao lại dùng 0.85 mà không phải 1.0?**
  - Tr: Để giải quyết bài toán "Spider Trap" (hai trang trỏ qua lại cho nhau mãi mãi). Con số 0.85 giúp thoát khỏi vòng lặp vô tận bằng cách cho phép người dùng "nhảy" sang trang khác.

---
*Chúc bạn có một buổi thuyết trình thành công rực rỡ!*
