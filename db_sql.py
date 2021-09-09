from psycopg2.extensions import SQL_IN
from pydantic.types import conset
import uvicorn
import logging
from typing import Optional,Callable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from connection import connect_to_db, close_db_connection

logger = logging.getLogger(__name__)

#create report data basic type
class Item(BaseModel):
    clientName: str
    coments: str
    detail_address: str
    goodsType: str
    stock_site: str
    stock_site_city: str
    phone: int
    sells_num: int
    user_address:dict
    #user_address: Any = Body(...) object
class ProItem(BaseModel):
    price: str
    productname: str
    repertory: str
    province:str
    stock: str

class StockItem(BaseModel):
    cityId: str
    prId: str

class GoodsItem(BaseModel):
    name: str

class SendListernClickDatas(BaseModel):
    action: str
    action_date: str
    base_Url:str
    content:str
    node_name: str
    userId: str
    userName: str
    hostname:str

class SendListernChangeDatas(BaseModel):
    action: str
    action_date: str
    old_Url:str
    new_Url:str
    userId: str
    userName: str
    hostname: str

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:9005",
    "http://localhost:9008",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def inter_order_datas(datas, user_id):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert order data **** ---")
    sql = "insert into user_order (CLIENTNAME, CLIENTID, COMENTS, GOODSTYPE, STOCK_SITE, STOCK_SITE_CITY, PHONE, SELLSNUM, PROVINCE,CITY, CITYAREA, STREET, DETAILADDRESS) \
                    values (%s, '%s',%s, %s, %s, %s, '%s', '%s', %s, %s, %s, %s, %s) RETURNING id"
    params = (datas.clientName, user_id, datas.coments, datas.goodsType, datas.stock_site, datas.stock_site_city, datas.phone, datas.sells_num, datas.user_address['province'][0], datas.user_address['province'][1], datas.user_address['province'][2],datas.user_address['street'], datas.detail_address) 
    cursor.execute(sql, params)
    order_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert order data **** ---")
    return order_id[0]

#creat a new user
async def inter_new_user(datas):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert one user data **** ---")
    sql = "insert into users (name, PHONE, PROVINCE, CITY, CITYAREA, detailaddress, sfc_role) \
             values(%s, '%s', %s, %s, %s, %s, %s) RETURNING id"
    params = (datas.clientName, datas.phone, datas.user_address['province'][0], datas.user_address['province'][1], datas.user_address['province'][2], datas.detail_address, '10')      
    cursor.execute(sql, params)
    user_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert one user data **** ---")

    return user_id[0]
#inter a new project 

async def inter_new_pro(datas):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert one user data **** ---")
    sql = "insert into product (productname, repertory, province, stock, price) \
             values(%s, %s, %s, %s, %s) RETURNING id"
    params = (datas.productname, datas.repertory, datas.province,datas.stock, datas.price)      
    cursor.execute(sql, params)
    pro_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert one pro data **** ---")
    return pro_id[0]

# add new goods
async def inter_new_goods(datas):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert one goods data **** ---")
    sql = "insert into goods_list (name) values('"+ datas.name+"') RETURNING id"

    cursor.execute(sql)
    good_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert goods data **** ---")
    return good_id[0]
    

async def inter_new_stockcity(datas):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert new stock data **** ---")
    sql = "insert into stock_site (city, province) \
             values(%s, %s) RETURNING city"
    params = (datas.cityId, datas.prId)      
    cursor.execute(sql, params)
    city_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert new stock data **** ---")
    return city_id[0]


async def check_exist_user(username, phone, city):
    exist_user = ""
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start checking user exist **** ---")
    sql = "select id from users where deleted='false' and name = %s and phone='%s' and city=%s"
    # 查询条件参数结束必须加,
    params = (username, phone, city,)
    
    cursor.execute(sql, params)
    while True:
        data = cursor.fetchone()
        if data == None:
            logger.warn("--- **** end checking user  **** ---")
            break
        exist_user = data[0]
    conn.commit()
    await close_db_connection(conn, cursor)
    if exist_user == "":
        exist_user = False
    return exist_user

async def check_exist_goodsname(name):
    exist_goodsid =""
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start checking goods exist **** ---")
    sql = "select name from goods_list  where name=%s"
    params = (name, )
    print(sql)
    cursor.execute(sql, params)
    while True:
        data = cursor.fetchone()
        if data == None:
            logger.warn("--- **** end goods pro  **** ---")
            break
        exist_goodsid = data[0]
    conn.commit()
    await close_db_connection(conn, cursor)
    if exist_goodsid == "":
        exist_goodsid = False
    return exist_goodsid

async def check_exist_city(id):
    exist_cityid =""
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start checking project exist **** ---")
    sql = "select city from stock_site  where city=%s and deleted='false'"
    params = (id, )
    print(sql)
    cursor.execute(sql, params)
    while True:
        data = cursor.fetchone()
        if data == None:
            logger.warn("--- **** end stock   **** ---")
            break
        exist_cityid = data[0]
    conn.commit()
    await close_db_connection(conn, cursor)
    if exist_cityid == "":
        exist_cityid = False
    return exist_cityid 

#get order list datas
async def get_stocks_list():
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start get stock site city list **** ---")
    sql = "select id, province , city ,deleted FROM stock_site "
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    await close_db_connection(conn, cursor)
    return data

#get product list datas
async def get_productdetial_list():
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start get product  list **** ---")
    sql = "select gl.name as productname, p.repertory, p.province, p.stock, p.price  FROM product p \
          left join goods_list gl on  cast(gl.id as  character varying)  = p.productname "
    # sql = "select productname , repertory, province, stock, price  FROM product where deleted = 'false'"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    logger.warn("--- **** get product end **** ---")
    await close_db_connection(conn, cursor)
    return data

#get one goods stock num
async def get_one_goods_stock_num(city, sid):
    has_goods = ""
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start get one goods max stock num **** ---")
    sql = "select p.stock, gl.name as productname, p.repertory, p.province, p.price  FROM product p \
          left join goods_list gl on  cast(gl.id as  character varying)  = p.productname \
          where p.repertory = %s and gl.id = %s"
    params = (city, sid,)
    print(sql)
    print(city)
    print(sid)
    cursor.execute(sql, params)
    while True:
        data = cursor.fetchone()
        if data == None:
            logger.warn("--- **** get one goods max stock num **** ---")
            break
        has_goods = data[0]
    conn.commit()
    await close_db_connection(conn, cursor)
    if has_goods == "":
        has_goods = False
    return has_goods

#get hot listener platfrom names

async def get_listener_host():
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start query listern platfrom name **** ---")
    sql = "select hostname from  listenuserdatas where deleted  = 'false' "
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end query listern platfrom name **** ---")
    return data

#get goods list datas
async def get_progoods_list():
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start get stock site city list **** ---")
    sql = "select id, name , createdata FROM goods_list where deleted ='false' "
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    await close_db_connection(conn, cursor)
    return data

#get stock list datas
async def getOrder():
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** Start get user order list **** ---")
    sql = "select  uo.clientid , uo.clientname ,uo.phone ,gl.name , uo.sellsnum, uo.detailaddress , uo.province , \
           uo.city, uo.status, u.is_members, uo.coments, uo.createdata, uo.stock_site, uo.stock_site_city from user_order uo \
           left join users u  on cast(u.id as  character varying) = uo.clientid \
           left join goods_list gl  on cast(gl.id as  character varying) = uo.goodstype   where u.deleted ='false' \
           order by uo.createdata desc "
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    await close_db_connection(conn, cursor)
    return data

#save the user listener datas
async def inter_listener_user_datas_click(datas):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert listener user data **** ---")
    sql = "insert into listenuserdatas (action, action_date, base_Url, content, node_name, userId, userName) \
            values(%s, %s, %s, %s, %s, %s, %s) RETURNING id"

    params = (datas.action, datas.action_date, datas.base_Url, datas.content, datas.node_name, datas.userId, datas.userName)    
    cursor.execute(sql, params)
    click_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert new stock data **** ---")
    return click_id[0]

#save the user listener datas
async def inter_listener_user_datas_change(datas):
    conn = await connect_to_db()
    cursor = conn.cursor()
    logger.warn("--- **** DB connect success **** ---")
    logger.warn("--- **** insert listener user data **** ---")
    sql = "insert into listenuserdatas (useraction, action_date, oldUrl, newUrl, userId, userName, hostname) \
           values(%s, %s, %s, %s, %s, %s, %s) RETURNING id"
    params = (datas.action, datas.action_date, datas.old_Url, datas.new_Url, datas.userId, datas.userName, datas.hostname)
    logger.warn(datas)
    logger.warn(sql)
    cursor.execute(sql, params)
    change_id = cursor.fetchone()
    conn.commit()
    await close_db_connection(conn, cursor)
    logger.warn("--- **** end insert new stock data **** ---")
    return change_id[0]



@app.get("/")
def read_root():
    return {"Hello": "World1"}

@app.get("/createdaily-report")
def test_root():
    return {"Hello": "Evan"}

@app.get("/getOrderDatas")
async def get_order_list():
    datas = await getOrder()
    return (datas)

@app.get("/getSiteDatas")
async def get_stock_list():
    datas = await get_stocks_list()
    return (datas)

@app.get("/productDatas")
async def get_products_list():
    datas = await get_productdetial_list()
    return (datas)

@app.get("/getGoodsDatas")
async def get_goods_list():
    datas = await get_progoods_list()
    return (datas)


#new stock
@app.post("/addnewStock")
async def submit_add_stock(request_data: StockItem):
        city_id = await check_exist_city(request_data.cityId)
        if city_id == False:
            # no exist pro id , add new project
            cityid = await inter_new_stockcity(request_data)
        else:
            cityid = False
            logger.warn("--- **** pro is exist !!  **** ---")
        return (cityid)

@app.post("/submitProjects")
async def submit_new_project(request_data: ProItem):
        proid = await inter_new_pro(request_data)
        return (proid)

@app.post("/addnewGoods")
async def submit_new_goods(request_data: GoodsItem):
        goods_id = await check_exist_goodsname(request_data.name)
        if goods_id == False:
            # no exist pro id , add new project
            goodsid = await inter_new_goods(request_data)
        else:
            goodsid = False
            logger.warn("--- **** pro is exist !!  **** ---")
        
        return (goodsid)

# @app.post("/getMaxStock")
# async def get_max_stocks(request_data: MaxStockItem):
#         max_stock = await get_one_goods_stock_num(request_data.city, request_data.sid)
#         return (max_stock)

@app.post("/sendlistenclick")
async def send_listen_click(request_data: SendListernClickDatas):
        logger.warn("get send test api start ")
        logger.warn(request_data)
        return (request_data)

@app.post("/sendlistenchange")
async def send_listen_chang(request_data: SendListernChangeDatas):
        logger.warn("get send test api start ")
        changed_id = await inter_listener_user_datas_change(request_data)
        return (changed_id)

@app.get("/getlistenhostname")
async def get_listener_hostname():
    datas = await get_listener_host()
    return (datas)


@app.get("/sendtestget")
async def get_test_get():
    datas = await get_progoods_list()
    return (datas)


@app.post("/submitReport")
async def send_reportData(request_data: Item):
        #sumbit the order data
        # 1 check if the user exist in data base if not create one
        user_id = await check_exist_user(request_data.clientName, request_data.phone, request_data.user_address['province'][1])
        if user_id == False:
           #insert a new user data if this is new user
           userid = await inter_new_user(request_data)
        else:
            userid = user_id
            logger.warn("--- **** User is exist !!  **** ---")
        # param: 1: city.
        # 2 sell stock num
        max_stock = await get_one_goods_stock_num(request_data.stock_site_city, request_data.goodsType)
        print(max_stock)
        if max_stock == False:
            userid = max_stock
            stockNum = max_stock
            stock_num = 0
            stock_val = 0
        else:
            stock_val = int(max_stock) - int(request_data.sells_num)
            if stock_val >= 0:
                stockNum = max_stock
                stock_num = int(max_stock)
                await inter_order_datas(request_data, userid)
            else:
                 userid = False
                 stockNum = stock_val
                 stock_num = int(max_stock)
        result = {
            "result": userid,
            "stockNum": stockNum,
            "stock_num": stock_num,
            "stock_val": stock_val
        }
        return (result)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

class Apihandler():
    async def test():
        re = await get_progoods_list()
        print(re)
        
