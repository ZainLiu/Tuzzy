# Tuzzy
参考gin和flask开发的一个webapp框架

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
    context.start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    print(f'hello:{context.params.get("name")}'.encode('utf-8'))
    context.respone = f'hello:{context.params.get("name")},v1'.encode('utf-8')
  
  # 初始化APP
  app = Engine()
  
  # 添加一个get请求的路由
  app.get("/hello/:name/haha", sayhello)
  
  # 启动服务
  app.run_http()
  ```

  

