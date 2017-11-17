# coding:utf-8
import smtplib
import email
import os.path


class SendAttachMail:
    def __init__(self, list_receiver, str_subject, str_msg, list_attach_file=[]):
        self.mail_host = "smtp.163.com"
        self.sender = "13052235539@163.com"
        self.subject = str_subject
        self.text_msg = str_msg
        self.list_receiver = list_receiver
        self.list_attach_file = list_attach_file
        self.server = smtplib.SMTP("smtp.163.com")
        self.server.login("13052235539@163.com", "a123456")

    def send_mail(self):
        # 构造MIMEMultipart对象做为根容器
        main_msg = email.MIMEMultipart.MIMEMultipart()
        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        text_msg = email.MIMEText.MIMEText(self.text_msg)
        main_msg.attach(text_msg)
        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        # 如果有附件添加附件
        for attach_file in list_attach_file:
            # 读入文件内容并格式化
            data = open(attach_file, 'rb')
            file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read())
            data.close()
            email.Encoders.encode_base64(file_msg)
            # 设置附件头
            basename = os.path.basename(attach_file)
            file_msg.add_header('Content-Disposition', 'attachment', filename=basename)
            main_msg.attach(file_msg)
            # 设置根容器属性
        main_msg['From'] = "<"+self.sender+">"
        main_msg['To'] = ";".join(self.list_receiver)
        main_msg['Subject'] = self.subject
        main_msg['Date'] = email.Utils.formatdate()
        # 得到格式化后的完整文本
        fullText = main_msg.as_string()
        # 用smtp发送邮件
        try:
            self.server.sendmail(self.sender, self.list_receiver, fullText)
        except Exception:
            pass
        finally:
            self.server.quit()

if __name__ == "__main__":
    list_receiver = ["zhangling@139erp.com", "linxiaowei@139erp.com"]
    str_subject = u"ERP-接口自动化报告"
    str_msg = "If you can't check the email's attachments, \n" \
              "please download them locally!"
    report_dir = os.getcwd()
    list_attach_file = []
    report_dir = os.path.dirname(report_dir)+"\\report"
    list_file = os.listdir(report_dir)
    for sfile in list_file:
        if sfile.endswith(".html") or sfile.endswith(".log"):
            list_attach_file.append(report_dir+"\\"+sfile)
    SendAttachMail(list_receiver, str_subject, str_msg, list_attach_file).send_mail()