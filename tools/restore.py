# استرجاع المصادر: python3 tools/restore.py <كلمة المرور> [مجلد الإخراج=src]
import sys,io,os,tarfile,hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pw=sys.argv[1].encode(); out=sys.argv[2] if len(sys.argv)>2 else "src"
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b=open(os.path.join(root,"vault","source.bin"),"rb").read()
salt,iv,ct=b[:16],b[16:28],b[28:]
key=hashlib.pbkdf2_hmac("sha256",pw,salt,310000,32)
data=AESGCM(key).decrypt(iv,ct,None)
tarfile.open(fileobj=io.BytesIO(data),mode="r:gz").extractall(out,filter="data")
print("تم الاسترجاع في",out)
