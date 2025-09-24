# Thiết kế AFL v0

## Mục tiêu
- Module hoá: indicators/, strategies/, utils/
- Tránh global trôi nổi; dùng tiền tố ind_/strat_/util_
- Rõ ràng đầu ra: `Buy`, `Sell`, `Short`, `Cover`, `PositionScore`

## API public
- Series output: `ind_*` cho indicators, `strat_*` cho strategy
- Tham số tối ưu: liệt kê tên, min/max/step

## Lưu ý AFL
- Sử dụng `SetOption` và `SetPositionSize` nhất quán
- Hạn chế `StaticVarSet`/`StaticVarGet`; nếu dùng, thêm tên dự án để tránh trùng