from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()


class DonHang(BaseModel):
    id: int                   
    ten_khach: str            
    san_pham: str            
    so_luong: int             
    gia: float                
    trang_thai: str = "moi"   
    thoi_gian: str = datetime.now().isoformat()  


database: List[DonHang] = []


# Lấy danh sách đơn hàng
@app.get("/donhang")
def get_danh_sach_don():
    return database

# Lấy chi tiết 1 đơn hàng
@app.get("/donhang/{ma_don}")
def get_don_hang(ma_don: int):
    for don in database:
        if don.id == ma_don:
            return don
    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

# Tạo mới đơn hàng
@app.post("/donhang")
def tao_don_hang(don: DonHang):
    database.append(don)
    return {"message": "Tạo đơn hàng thành công!", "don_hang": don}

# Cập nhật đơn hàng
@app.put("/donhang/{ma_don}")
def cap_nhat_don(ma_don: int, don_moi: DonHang):
    for i, don in enumerate(database):
        if don.id == ma_don:
            database[i] = don_moi
            return {"message": "Cập nhật thành công!", "don_hang": don_moi}
    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

# Xoá đơn hàng
@app.delete("/donhang/{ma_don}")
def xoa_don_hang(ma_don: int):
    for don in database:
        if don.id == ma_don:
            database.remove(don)
            return {"message": "Xoá đơn hàng thành công!"}
    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
