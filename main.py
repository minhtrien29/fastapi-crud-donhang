from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

#class order cho ng quan li don hang
class Order(BaseModel):
    id: int #id 
    customer_name: str #ten khach hang
    product_name: str #ten san pham
    quantity: int #sl
    price: float #gia

#class order cua khach hang khi tao don hang moi
class OrderCreate(BaseModel): 
    customer_name: str #ten khach hang
    product_name: str #ten san pham
    quantity: int #sl
    price: float #gia 

class OrderResponse(BaseModel):# tao class de tra ve thong bao va don hang
    message: str
    order: Order

order_db: List[Order] = [] #ds don hang luu tam thoi
current_id: int = 1  # id tu tang cho cac don hang

# --- CRUD ---

# CREATE: tao don hang

@app.post("/orders", response_model=OrderResponse, status_code=201) #khai bao duong dan
def create_order(order: OrderCreate): # ham va ten ham khai bao don hang moi cua khach
    global current_id # su dung bien id
    new_order = Order(id=current_id, **order.dict()) #tao don hang moi, voi id tu tao, cac thuoc tinh con lai lay tu order
    order_db.append(new_order) #them don hang moi vao db
    current_id += 1 #id tang them 1 cho don hang tiep theo
    return OrderResponse(
        message= "Tạo đơn hàng thành công",
        order= new_order
    ) # tra ve don hang moi duoc khach tao
# READ: lay tat ca don hang

@app.get("/orders", response_model=List[Order]) #khai bao duong dan lay tat ca don hang
def get_orders(): # ham va ten ham lay don
    return order_db # tra ve ds don hang

# READ: lay don hang theo ID
@app.get("/orders/{order_id}", response_model=OrderResponse) #khai bao duong dan lay don hang theo ID cua server
def get_order(order_id: int): # ham va ten ham lay don hang theo ID
    for order in order_db: # lay don hang trong ds 
        if order.id == order_id: # neu id don hang trung 
            return OrderResponse(
                message= "Đon hàng được đặt thành công",
                order= order
            ) # tra ve don hang
    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng") # kh tim thay don vi trung id

# UPDATE: cap nhat don hang cua khach theo ID

@app.put("/orders/{order_id}", response_model=OrderResponse) #khai bao duong dan de cap nhat don hang cua server
def update_order(order_id: int, updated_order: OrderCreate): #ham va ten ham cap nhat don hang cua khach da dat
    for idx, order in enumerate(order_db): #dat bien idx de lay dung don hang can cap nhat, co idx thi kh bi nham don hang
        if order.id == order_id: #trung id can upddate
            new_order = Order(id=order_id, **updated_order.dict()) # don hang moi lay id da tao va cap nhat cac thuoc tinh don hang khach dat
            order_db[idx] = new_order #ds don hang chua bien idx de cap nhat gio tro thanh don hang moi
            return OrderResponse(
                message= "Đơn hàng của bạn đã được cập nhật thành công",
                order= new_order
            ) # tra ve don hang da cap nhat
    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng") # neu id kh trung

# DELETE: xoa don hang theo ID

@app.delete("/orders/{order_id}") #khai bao duong dan de xoa don hang
def delete_order(order_id: int): #ham va ten ham de xoa don hang
    for idx, order in enumerate(order_db): #voi don hang duoc update dung de lay dung don can xoa
        if order.id == order_id: #neu id don trung
            order_db.pop(idx) #xoa don hang idx chinh xac
            return {"message": "Xóa đơn hàng thành công"} #hien tb sau khi xoa 
    raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng") #neu id kh trung 
