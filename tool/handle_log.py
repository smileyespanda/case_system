# coding:utf-8
list_msg = []

print_info = True
print_warning = True
print_error = True
log_path = "app.log"


def build_log(msg):
    list_msg.append(msg)


def output_log():
    f = open(log_path, "wb")
    for msg in list_msg:
        if msg.startswith('<info>') and print_info:
            f.write(msg.encode())
        elif msg.startswith('<error>') and print_error:
            f.write(msg.encode())
        elif msg.startswith('<warning>') and print_warning:
            f.write(msg.encode())
    f.close()

