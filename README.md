# Tuzzy
参考gin和flask开发的一个webapp框架

##### 简单使用

```
# 导入app引擎
from tuzzy import Engine

# 初始化APP
app = Engine()
# 添加一个get请求的路由
app.get("/hello/:name/haha", sayhello)
# 启动服务
py_gee.run_http()
```

