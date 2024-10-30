import pyotp

secret = "YJBJSBQT3EJB4CEW"
# 使用密钥创建TOTP对象
totp = pyotp.TOTP(secret)

while True:
    # 获取当前的一次性密码
    otp = totp.now()
    print("\rOne - Time Password:", otp, end="")