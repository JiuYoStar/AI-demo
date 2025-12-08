### 重启php

1、用agentuser进入到容器

>   docker exec -it -uagentuser webapps1 /bin/bash

2、重启php

>   /dragonball/scripts/stop.d/2_stop_php.sh && /dragonball/scripts/start.d/2_start_php.sh

通过 **php-fpm + Nginx/Apache** 的方式运行

如果服务挂掉、页面 500、无响应，你就需要来这里看看脚本是否启动成功。



### 调试模式

1.   研发环境

```shell
# 修改 /web/php/config/core.config.php 中代码
define('_DEBUG', 'N');  → define('_DEBUG', 'Y');
# 直接在页面输出报错（Notice / Warning / Fatal）
# 禁止在生产环境这么配置
```

2.   调试函数

```php+HTML
echo "<pre>";
var_dump($value);
echo "</pre>";
```

3.   应用日志

```shell
log::debug("xxxx");
log::info("yyyy");

输入的日志所在目录: /dragonball/dirmap/log/php/access
```

4.   php服务日志

```shell
tail -f /dragonball/dirmap/log/php/php-fpm.log
# 如果发现 502、No input file、FastCGI error，这里是排查入口。
• 服务是否启动成功
• 端口冲突
• 内存溢出
• worker 进程异常退出
```

5.   确认php服务是否正常

```shell
ps -ef | grep php-fpm
sh /dragonball/scripts/start.d/2_start_php.sh # 如果服务启动失败, 需要手动执行一下
```

6.   查看php错误日志

```shell
# 如果看不到任何输出, 查看 ↓
/dragonball/dirmap/log/php/php-fpm.log
```

7.   查看业务日志

```shell
目录 → /dragonball/dirmap/log/php/access
tail -f /dragonball/dirmap/log/php/access
```













