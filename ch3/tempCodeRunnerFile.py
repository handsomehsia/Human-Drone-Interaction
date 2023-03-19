import threading

## 基本用法 --------------------------------------------------- #


def job(name):  # 要被執行的方法(函數)
    print("HI " + name)


# 放入執行序中
t = threading.Thread(target=job, args=('Nash',))

t.start()  # 開始

t.join()  # 等待結束
