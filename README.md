# nonebot-plugin-practice

使用和风天气api来编写天气插件实现简单的天气查询功能

# 安装

使用 `git clone ` 进行安装到 `nonebot2` 的 `plugins` 文件夹下

# 指令

`/天气+地区`   
例如：`/天气上海` 或者 `/天气 上海`

# 配置

## apikey 必须配置 环境配置

```
WEATHER_API_KEY=你的apikey
```

## APIKEY 获取方式

**1、注册和风天气账号**  
进入官网注册[https://id.qweather.com/#/login](https://id.qweather.com/#/login)  
**2、进入控制台**  
登录后，点击 “和风天气开发者控制台”  
**3、创建项目**  
点击控制台左侧 “项目管理”，然后点击 “创建项目”，根据提示自行填写  
“选择订阅” -> “免费订阅”，“设置 KEY” -> “Web API”，都填好后“创建”  
**4、获取 key 并配置.env.xx**  
返回 “项目管理”，可以看到创建的项目，点击 KEY 下面的 “查看”，复制 KEY 到你的.env.xx 即可。

