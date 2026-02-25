# Pipes Puzzle - AI Solver

Ứng dụng giải trò chơi Pipes Puzzle (5×5) bằng nhiều thuật toán tìm kiếm AI: DFS, BFS, A* và Simulated Annealing.

---

## Yêu cầu hệ thống

- **Python 3.x** (khuyến nghị 3.8+)
- **tkinter** – thường đi kèm Python
- **matplotlib** – vẽ biểu đồ thống kê

### Cài đặt phụ thuộc

```bash
pip install matplotlib
```

---

## Cách chạy

### Phiên bản GUI (tkinter)

1. Mở terminal tại thư mục `Pipes_Puzzle`.
2. Chạy:

```bash
python main.py
```

3. Cửa sổ giao diện hiện ra với bảng 5×5 ở giữa.

### Phiên bản Web

1. Cài Flask: `pip install flask`
2. Mở terminal tại thư mục `Pipes_Puzzle`.
3. Chạy:

```bash
python web/app.py
```

4. Mở trình duyệt truy cập: **http://localhost:5000**

---

## Tổng quan mã nguồn

### Cấu trúc thư mục

```
Pipes_Puzzle/
├── main.py              # Điểm vào GUI (tkinter)
├── data.py              # Dữ liệu test (8 mức: level 0–7)
├── data1.py             # Dữ liệu test thay thế (10 mức, có mức không giải được)
├── solver/              # Module thuật toán
│   ├── base_solver.py
│   ├── state_and_node.py
│   ├── bfs_solver.py
│   ├── dfs_solver.py
│   ├── astar_solver.py
│   └── sa_solver.py
├── ui/                  # Giao diện
│   ├── main_window.py
│   ├── board_view.py
│   ├── control_panel.py
│   ├── diagnostics_panel.py
│   └── components.py
├── performance/         # Đo thời gian và bộ nhớ
└── web/                 # Phiên bản web (Flask)
    ├── app.py           # Flask API: /api/solve, /api/levels, /api/initial/<level>
    └── static/          # index.html, style.css, app.js
    ├── timer.py
    └── memory.py
```

---

## Luật chơi và định dạng dữ liệu

### Mục tiêu

Xoay các ô ống (chỉ thay đổi góc quay, không đổi loại ống) sao cho **nước từ ô trung tâm (2,2) chảy đầy cả 25 ô**.

- **Ô trung tâm (2,2)**: van nước, luôn có nước.
- **Ô có nước**: màu xanh dương (`#5DADE2`).
- **Ô không có nước**: màu trắng.
- **Giải xong**: `countBump == 25` (25 ô đều có nước).

### Loại ống

| `type` | Tên             | Số hướng | Mô tả                    |
|--------|-----------------|----------|---------------------------|
| 1      | Dead-end        | 1        | Ống cụt                   |
| 2      | Straight        | 2        | Ống thẳng (ngang/dọc)     |
| 3      | Elbow           | 2        | Ống góc vuông             |
| 4      | T-joint         | 3        | Ống chữ T                 |

### Hướng (`heading`)

- `0` → Đông (>)  
- `90` → Nam (v)  
- `180` → Tây (<)  
- `270` → Bắc (^)

### Hệ tọa độ

- Gốc `(0,0)` ở góc **dưới-trái**.
- `x` tăng hướng lên, `y` tăng hướng sang phải.

Mỗi ô là dict: `{"type": int, "heading": int}`; khi tính toán thêm trường `"bump": bool` (có nước hay không).

---

## Thuật toán giải

### 1. DFS (Depth-First Search)

- Dùng `open_list` (ngăn xếp), `visited` set.
- Lấy trạng thái từ cuối danh sách.
- Tạo successors bằng cách xoay từng ô với các góc 0°, 90°, 180°, 270°.
- Không đảm bảo tìm lời giải tối ưu, có thể chậm trên bản đồ lớn.

### 2. BFS (Breadth-First Search)

- Dùng `deque` làm hàng đợi, `visited` set.
- Lấy trạng thái từ đầu hàng đợi.
- Luôn tìm được lời giải **ngắn nhất** (ít bước xoay nhất).

### 3. A\*

- Dùng hàng đợi ưu tiên (heap) với hàm đánh giá `f(n) = g(n) + h(n)`:
  - `g(n)`: chi phí đã đi (số bước × 2).
  - `h(n)`: heuristic – khuyến khích số ô có nước nhiều, ưu tiên biên và tránh vòng lặp.
- Hàm `hx()`:
  - Phạt nếu số ô có nước ít.
  - Thưởng nếu ô biên hướng ra ngoài.
  - Phạt nặng khi tạo vòng kín (`checkRecursionBump`).

### 4. Simulated Annealing (SA)

- Thuật toán heuristic, không đảm bảo tìm lời giải.
- Tham số mặc định: `initial_temp=500`, `cooling_rate=0.9995`, `min_temp=0.001`, `max_iterations=80000`.
- Mỗi bước chọn ngẫu nhiên một ô, xoay sang hướng hợp lệ khác.
- Chấp nhận bước mới nếu tốt hơn, hoặc theo xác suất `exp(-Δ/T)` khi tệ hơn.
- Mục tiêu tối thiểu: `25 - countBump = 0`.

---

## Module chính

### `state_and_node.py`

- **`State`**: Ma trận 5×5 + logic lan truyền nước (`bumpWater`), kiểm tra kết nối với trung tâm, phát hiện vòng lặp.
- **`Node`**: Nút tìm kiếm gồm `State`, bước xoay (`rotate`), tham chiếu `previous`.
- **`generate_successors(node)`**: Sinh các trạng thái kế tiếp bằng cách xoay từng ô (trừ trường hợp trùng hướng, hoặc ống thẳng chỉ có 2 hướng).

### `ui/main_window.py` – `PipesGUI`

- Ghép bảng (`BoardView`), bảng điều khiển (`ControlPanel`), bảng thống kê (`DiagnosticsPanel`).
- Xử lý Solve / Stop / Reset, chọn level và thuật toán.
- Gọi solver với `step_callback`, đo thời gian và bộ nhớ qua `PerformanceTracker`.

### `ui/board_view.py` – `BoardView`

- Vẽ lưới 5×5 và từng ống theo `type` + `heading`.
- Ống có nước màu xanh, không có nước màu trắng; ô trung tâm có dấu đỏ.

### `ui/control_panel.py` – `ControlPanel`

- Chọn thuật toán: DFS, BFS, A*, Simulated Annealing.
- Chọn level từ `data.TESTCASE`.
- Nút Solve, Stop, Reset và điều khiển Prev/Next cho từng bước.
- Tùy chọn “Show steps” và thanh tốc độ animation.

### `ui/diagnostics_panel.py` – `DiagnosticsPanel`

- Hiển thị số bước hiện tại / tổng số bước.
- Hiển thị số trạng thái đã khám phá, thời gian chạy, bộ nhớ đỉnh.
- Nút “Plot Statistic” vẽ biểu đồ phân bố số trạng thái theo độ sâu (A* và SA).

---

## Nguồn dữ liệu test

- **`data.py`**: 8 mức (level 0–7), đều có lời giải.
- **`data1.py`**: 10 mức:
  - 1–5: có lời giải.
  - 6–8: các dạng không giải được (góc tách biệt, toàn ống thẳng, v.v.).

Ứng dụng mặc định dùng `data.py`. Để đổi sang `data1.py`, sửa import trong `main_window.py`.

---

## Điều khiển giao diện

| Hành động | Cách thực hiện |
|-----------|-----------------|
| Giải puzzle | Chọn thuật toán và level → Solve |
| Dừng giải | Stop |
| Đưa về ban đầu | Reset |
| Xem từng bước | Bật “Show steps”, sau khi giải xong dùng Prev / Next |
| Điều chỉnh tốc độ | Thanh “Speed (ms)” – giá trị lớn = chậm hơn |
| Xem biểu đồ | Sau khi dùng A* hoặc SA, bấm “Plot Statistic” |

---

## Lưu ý kỹ thuật

1. **Ống thẳng (type 2)**: chỉ có 2 hướng khác nhau (0/180 hoặc 90/270). `generate_successors` bỏ qua các hướng trùng.
2. **So sánh trạng thái**: `State` triển khai `__hash__` và `__eq__` dựa trên `heading` và `bump` để dùng trong `visited` set.
3. **Hiệu suất**: BFS dùng `deque` thay cho list để `popleft()` có độ phức tạp O(1).
4. **Dừng sớm**: Solver kiểm tra `_stopped` trong vòng lặp; giao diện có thể gọi Stop để dừng giải.
