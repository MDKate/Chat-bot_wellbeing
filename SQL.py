import sqlite3 as sq

async def db_start():
    global db, cur
    db = sq.connect('new.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS base(user_id TEXT, count TEXT, city TEXT, page TEXT, ChoosingTopicsResult TEXT, firstResult TEXT, endSlinding TEXT, slindingResult TEXT, nextPage TEXT, nextPage1 TEXT, nextPageDS TEXT, SecondResult TEXT, SlidingLevelTupe4Result TEXT, endSecond TEXT, slindingType5Result TEXT, s TEXT,  cep TEXT, typGen TEXT, cepType TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS logs(user_id TEXT, date TEXT, time TEXT, req TEXT)")
    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM base WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO base VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, 0, '', 0, '', '', '', '', '', '', '', '', '', '', '', 0, '', '', ''))
        db.commit()

async def logs_insert(user_id, date, time, req):
    # user = cur.execute("SELECT 1 FROM logs WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    # if not user:
    cur.execute(f"INSERT INTO logs VALUES(?, ?, ?, ?)", (user_id, date, time, req))
    db.commit()


async def edit_profile(name, value,  user_id):
    # async with state.proxy() as data:
    #     cur.execute("UPDATE  base SET count  = '{}', city  = '{}', page  = '{}', ChoosingTopicsResult = '{}', firstResult = '{}', endSlinding = '{}', slindingResult = '{}', nextPage = '{}', nextPage1 = '{}', nextPageDS = '{}', SecondResult = '{}', SlidingLevelTupe4Result = '{}', endSecond = '{}', slindingType5Result = '{}', s = '{}',  cep = '{}', typGen = '{}', cepType = '{}' WHERE user_id == '{}'".format(
    #         data['count'], data['city'], data['page'], data['ChoosingTopicsResult'], data['firstResult'], data['endSlinding'], data['slindingResult'], data['nextPage'], data['nextPage1'], data['nextPageDS'], data['SecondResult'], data['SlidingLevelTupe4Resul'], data['endSecond'], data['slindingType5Result'], data['s'],  data['cep '], data['typGen'], data['cepType'], user_id))
    cur.execute(f'''UPDATE base SET {name} = ? WHERE user_id = ?''', (value, user_id))
    db.commit()


async def count_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT count FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    # await result[0]
    return result[0] if result else None

async def city_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT city FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def page_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT page FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def ChoosingTopicsResult_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT ChoosingTopicsResult FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None


async def firstResult_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT firstResult FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def endSlinding_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT endSlinding FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def slindingResult_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT slindingResult FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def nextPage_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT nextPage FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def nextPage1_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT nextPage1 FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def nextPageDS_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT nextPageDS FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def SecondResult_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT SecondResult FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def SlidingLevelTupe4Result_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT SlidingLevelTupe4Result FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def endSecond_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT endSecond FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def slindingType5Result_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT slindingType5Result FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def s_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT s FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def cep_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT cep FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def typGen_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT typGen FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None

async def cepType_value_from_db(user_id):
    # cursor = db.cursor()
    cur.execute("SELECT cepType FROM base WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None