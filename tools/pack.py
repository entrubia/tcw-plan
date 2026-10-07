# تشفير المصادر: python3 tools/pack.py <كلمة المرور> [مجلد المصادر=src]
import sys,io,os,tarfile,hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pw=sys.argv[1].encode(); src=sys.argv[2] if len(sys.argv)>2 else "src"
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode="w:gz") as t:
    for n in sorted(os.listdir(src)):
        t.add(os.path.join(src,n),arcname=n,filter=lambda i:None if i.name.endswith("pw.txt") or "__pycache__" in i.name else i)
salt,iv=os.urandom(16),os.urandom(12)
key=hashlib.pbkdf2_hmac("sha256",pw,salt,310000,32)
os.makedirs(os.path.join(root,"vault"),exist_ok=True)
open(os.path.join(root,"vault","source.bin"),"wb").write(salt+iv+AESGCM(key).encrypt(iv,buf.getvalue(),None))
print("تم التشفير:",len(buf.getvalue())//1024,"KB")
