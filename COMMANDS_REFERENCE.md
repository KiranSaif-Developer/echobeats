# EchoBeats — Saari Commands (Reference File)

⚠️ **Sabse zaroori baat:** neeche do tarah ki commands hain —
- **CMD commands** → normal `C:\...>` prompt pe chalti hain
- **SQL/psql commands** → sirf `psql` ke andar (`postgres=#` ya `echobeats=#` prompt) chalti hain

Dono ko mix mat karna — yahi sabse zyada confusion ki wajah bani thi.

---

## 1️⃣ Database Setup (sirf ek baar karna hai)

**CMD mein (normal prompt pe):**
```
cd "C:\Users\Zaka ullah\.gemini\antigravity\scratch\echobeats"
psql -U postgres -f 01_create_db.sql
psql -U postgres -d echobeats -f 02_tables_and_data.sql
```

**Verify karne ke liye — psql ke andar jao:**
```
psql -U postgres -d echobeats
```
Phir psql ke andar (SQL commands):
```sql
\dt
```
→ 8 tables dikhne chahiye (users, songs, playlists, playlist_songs, follows, likes, comments, listening_history)

**psql se bahar niklo:**
```sql
\q
```

---

## 2️⃣ Backend Setup (sirf pehli baar karna hai)

**CMD mein:**
```
cd "C:\Users\Zaka ullah\.gemini\antigravity\scratch\echobeats"
pip install -r requirements.txt
```

**`.env` file banao (agar pehle nahi bani):**
```
copy .env.example .env
```
Phir `.env` ko Notepad mein khol kar `DB_PASSWORD=` ke aage apna real Postgres password likho, save karo.

---

## 3️⃣ Backend Chalana (har baar jab kaam karna ho)

**CMD mein:**
```
cd "C:\Users\Zaka ullah\.gemini\antigravity\scratch\echobeats"
python app.py
```

Server band karna ho to:
```
Ctrl + C
```

**Browser mein test karne ke liye:**
```
http://localhost:5000
http://localhost:5000/api/songs
```

---

## 4️⃣ Database Ko Direct Check Karna Ho (optional)

**CMD mein psql kholo:**
```
psql -U postgres -d echobeats
```

**Ab psql ke andar (SQL commands):**
```sql
\dt
SELECT * FROM songs;
SELECT * FROM users;
```

**psql se bahar aane ke liye:**
```sql
\q
```

---

## 🛑 Common Mistakes (jo humare saath hui, dobara na ho)

1. **`psql` ke andar cmd commands (`cd`, `pip`, `python`) chalana** → error dega ya atak jayega. Pehle `\q` se bahar niklo.
2. **Prompt `postgres-#` ya `echobeats-#` (dash ke saath) dikhe** → matlab psql ek adhoora command wait kar raha hai. Sirf `;` type karke Enter dabao, phir `\q`.
3. **`.env.example` ko `.env` na banana** → backend password load nahi kar payega, "password authentication failed" error aayega. `copy .env.example .env` chalana zaroori hai (ya rename kar do).
4. **`DROP DATABASE` / `CREATE DATABASE` ko dusre SQL statements ke sath ek hi transaction/script mein chalana (pgAdmin Query Tool mein)** → error dega. Inhe hamesha standalone chalao.
5. **Multiple commands ek sath paste karna bina Enter ke beech mein** → psql confuse ho jata hai. Ek-ek command, Enter dabate hue chalao.

---

## 📁 Project Folder Structure (final)
```
echobeats/
├── .env                  (real password — kabhi share na karo)
├── .env.example
├── 01_create_db.sql
├── 02_tables_and_data.sql
├── app.py
├── auth_utils.py
├── db.py
├── README.md
├── requirements.txt
└── routes/
    ├── __init__.py
    ├── auth.py
    ├── songs.py
    └── playlists.py
```
1. Backend folder mein jao:
cd "C:\Users\Zaka ullah\.gemini\antigravity\scratch\echobeats"
2. Confirm karo files sahi hain:
dir
(.env, app.py, db.py, requirements.txt, aur routes folder dikhne chahiye)
3. Dependencies install karo (sirf pehli baar zaroori, phir dubara nahi karna):
pip install -r requirements.txt
4. Server chalao:
python app.py
5. Browser mein test karo:
http://localhost:5000
http://localhost:5000/api/songs
6. Server band karna ho to:
Ctrl + C

Yaad rakhne wali baatein (taake purane masle dobara na ho):

Ye saari commands normal C:\...> prompt pe chalani hain — agar prompt postgres=# ya echobeats=# dikhe, matlab tum galti se psql ke andar ho, wahan ye commands nahi chalengi. psql se nikalne ke liye \q type karo.
Agar kabhi psql se seedha database check karna ho:

psql -U postgres -d echobeats
uske andar sirf SQL commands (jaise \dt, SELECT * FROM songs;) chalani hain, cmd commands nahi.
Isay ek Notepad file mein save kar lo apne paas — jab bhi naya session shuru karo, bas step 1, 4, 5 chalane hain (2 aur 3 sirf verify/pehli baar ke liye hain).