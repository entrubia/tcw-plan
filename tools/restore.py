# استرجاع المصادر: python3 tools/restore.py <كلمة المرور> [مجلد الإخراج=src]
# 1) نزّل أحدث نسخة من الفرع backup إلى vault/source.bin:
#    gh api -H "Accept: application/vnd.github.raw" "repos/entrubia/tcw-plan/contents/source.bin?ref=backup" > vault/source.bin
# 2) شغّل هذا الملف من جذر المستودع؛ يفك المصادر ثم يعيد بناء site/media من ملفات d/
import sys,io,os,tarfile,hashlib,json,shutil
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pw=sys.argv[1].encode(); out=sys.argv[2] if len(sys.argv)>2 else "src"
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b=open(os.path.join(root,"vault","source.bin"),"rb").read()
salt,iv,ct=b[:16],b[16:28],b[28:]
key=hashlib.pbkdf2_hmac("sha256",pw,salt,310000,32)
tarfile.open(fileobj=io.BytesIO(AESGCM(key).decrypt(iv,ct,None)),mode="r:gz").extractall(out,filter="data")
site=os.path.join(out,"site"); mp=os.path.join(site,"media_map.json")
if os.path.exists(mp):
    ssalt=bytes.fromhex(open(os.path.join(site,"site_salt.hex")).read().strip())
    A=AESGCM(hashlib.pbkdf2_hmac("sha256",pw,ssalt,310000,32))
    md=os.path.join(site,"media"); os.makedirs(md,exist_ok=True)
    miss=0
    for f,i in json.load(open(mp)).items():
        p=os.path.join(root,"d",i+".bin")
        if not os.path.exists(p): miss+=1; continue
        e=open(p,"rb").read(); open(os.path.join(md,f),"wb").write(A.decrypt(e[:12],e[12:],None))
    shutil.copy(os.path.join(root,"logo.png"),os.path.join(md,"logo.png"))
    print("الوسائط:",len(os.listdir(md)),"ملف" + (f" · مفقود {miss}" if miss else ""))
print("تم الاسترجاع في",out)
