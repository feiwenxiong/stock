# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
import os
import time
import akshare as ak
from hot_stock import *
from tabulate import tabulate
#os.system("sudo mount -a")
# def mail(t,recipients,fileName):
#     ret=True
#     try:
#         msg=MIMEText(t,'plain','utf-8')
#         msg['From']=formataddr(["Jack",my_sender])          # 括号里的对应发件人邮箱昵称、发件人邮箱账号
#         msg['To'] = ', '.join(formataddr(["Recipient", r]) for r in recipients)            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
#         msg['Subject']="instock system daily report"                   # 邮件的主题，也可以说是标题
#         server=smtplib.SMTP("smtp.qq.com", 587)             # 发件人邮箱中的SMTP服务器，端口是587
#         server.login(my_sender, my_pass)                    # 括号中对应的是发件人邮箱账号、邮箱密码
#         server.sendmail(my_sender,recipients,msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
#         server.quit()  # 关闭连接
#     except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
#         ret=False
#     return ret


from tabulate import tabulate

def mail(t, recipients, folder_path=None, xlsx_file=None, df=None):
    ret = True
    try:
        # 创建MIME多部分消息对象
        msg = MIMEMultipart("alternative")
        msg['From'] = formataddr(["Jack", my_sender])          # 发件人邮箱昵称、发件人邮箱账号
        msg['To'] = ', '.join(formataddr(["Recipient", r]) for r in recipients)  # 收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "instock system daily report"         # 邮件的主题

        # 总是添加纯文本内容
        # text_part = MIMEText(t, 'plain', 'utf-8')
        # msg.attach(text_part)

        # 如果提供了数据，则创建一个DataFrame并转换为HTML表格
        if df is not None:
            # df = pd.DataFrame(data)
            html_content = df.to_html(index=False)
            # 创建HTML部分
            html_part = f"""
            <html>
              <body>
                <p>{t}</p>
                <br>
                {html_content}
              </body>
            </html>
            """
            part = MIMEText(html_part, 'html', 'utf-8')
            msg.attach(part)

        # 如果提供了文件夹路径，则添加该路径下所有的.xlsx附件
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.endswith('.xlsx'):
                    filepath = os.path.join(folder_path, filename)
                    with open(filepath, "rb") as file:
                        xlsx_part = MIMEApplication(file.read(), Name=filename)
                        xlsx_part['Content-Disposition'] = f'attachment; filename="{filename}"'
                        msg.attach(xlsx_part)
                elif  filename.endswith('.svg'):
                    filepath = os.path.join(folder_path, filename)
                    with open(filepath, "rb") as file:
                        svg_part = MIMEApplication(file.read(), Name=filename)
                        svg_part['Content-Disposition'] = f'attachment; filename="{filename}"'
                        msg.attach(svg_part)


        # 如果提供了单个xlsx文件路径，则添加xlsx附件
        elif xlsx_file:
            with open(xlsx_file, "rb") as file:
                xlsx_part = MIMEApplication(file.read(), Name=xlsx_file.split('/')[-1])
                xlsx_part['Content-Disposition'] = f'attachment; filename="{xlsx_file.split("/")[-1]}"'
                msg.attach(xlsx_part)

        # 发送邮件
        server = smtplib.SMTP("smtp.qq.com", 587)  # 发件人邮箱中的SMTP服务器，端口是587
        server.starttls()                          # 启用TLS加密
        server.login(my_sender, my_pass)           # 发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, recipients, msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()                              # 关闭连接
    except Exception as e:
        print(f"An error occurred: {e}")
        ret = False
    return ret


if __name__ == "__main__":  
    # 设置发件人和收件人信息
    my_sender='feiwenxiong@foxmail.com'  # 自己的邮箱账号
    my_pass = 'yigznphogjsnbiea'   # 发件人邮箱密码(之前获取的授权码)
    recipients = [my_sender,"xzliao96@163.com"]
   
    
   #######################################################################################
    #涨停+情绪数据
    #添加附件
    send_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)),"send")
    
   #添加text
    emx = earn_money_xiaoying()
    # print(emx)
    t = str(emx)
    
    #添加表格
    from hot_stock import kongpan_attention
    df = kongpan_attention()
    
    
    #######################################################################################
    
    ret = mail(t,recipients,folder_path=send_folder,df=df)
    if ret:
        print("发送邮件成功")
    else:
        mail(t,recipients)
        print("发送邮件失败")