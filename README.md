# Tuzzy
参考gin和flask开发的一个webapp框架, 实现了动态路由，路由分组和中间件功能，本地环境用werkzeug的run_simple启动，线上建议使用uwsgi

##### 简单使用

+ 安装依赖包

  ```shell
  pip install werkzeug
  ```

+ 示例代码

  ```python
  # 导入app引擎
  from tuzzy import Engine
  
  # 处理视图
  def sayhello(context):
    context.json({"name": context.params.get("name"), "message": "你好呀"})
  
  # 初始化APP
  app = Engine()
  
  # 添加一个get请求的路由
  app.get("/hello/:name/haha", sayhello)
  
  # 启动服务
  app.run_http()
  ```

  

