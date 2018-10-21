+ https https://www.jianshu.com/p/45a1003b2b55
+ cloudflare
+ secret key
+ 服务器ssh，ssh database
+ git提交自動發佈（github備份，静态页面git page）
+ 301重定向
+ 数据库备份


####link:
+ models: id, title, links_category, url(unique)
+ links management: edit, delete
+ new link form:string(name), select(cate), string(href)
####linkCategory:
+ models: id, name(default)
+ management
+ new category
####book
+ models: id, name, books_category, comments(ckteditor),timestamp
+ books manage: edit, delete
+ new book form: name, category, comments
+ book detail
####bookCategory
+ models: id, name
+ management
+ new category

models->forms->templates->views->migrate->fake data

[markdown语法](https://github.com/younghz/Markdown)

+ 生成rsa
+ 修改config
+ 上传到服务器，修改目录权限700， 文件权限600
+ 修改服务器config，重启服务


+ 新建数据库
+ 修改数据库连接url
+ 修改setting
