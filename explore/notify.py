# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
import time
#os.system("sudo mount -a")
def mail(t,recipients):
    ret=True
    try:
        msg=MIMEText(t,'plain','utf-8')
        msg['From']=formataddr(["Jack",my_sender])          # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = ', '.join(formataddr(["Recipient", r]) for r in recipients)            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="instock system daily report"                   # 邮件的主题，也可以说是标题
        server=smtplib.SMTP("smtp.qq.com", 587)             # 发件人邮箱中的SMTP服务器，端口是587
        server.login(my_sender, my_pass)                    # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,recipients,msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret



if __name__ == "__main__":  
    # 设置发件人和收件人信息
    my_sender='feiwenxiong@foxmail.com'  # 自己的邮箱账号
    my_pass = 'yigznphogjsnbiea'   # 发件人邮箱密码(之前获取的授权码)
    
    import akshare as ak
    from hot_stock import *
    emx = earn_money_xiaoying()
    # print(emx)
    t = str(emx)
    recipients = [my_sender,"xzliao96@163.com"]

    ret=mail(t,recipients)
    if ret:
        print("发送邮件成功")
    else:
        mail(t,recipients)
        print("发送邮件失败")