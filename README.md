# go_moso

蓝墨云刷分工具

使用方法：

1.打开config.py

更改articleId为你的蓝墨云活动id

更改courseId为你的蓝墨云班级id

以上两部分的教程在这:https://www.ailoli.org/archives/50/

更改values下的accout_name为你的蓝墨云账号

更改values下的user_pwd为你的蓝墨云密码

更改article_id为你的蓝墨云班级活动id

更改sleepNumber为你需要的睡眠时间

k变量说明：

k变量为概率性变量：

k的数值代表循环次数，每次循环都会自动从ABCD中随机选择一个，设为0则不执行

设的越高分数理论上来讲会越低（不排除人品特别好的）

总的来说这个变量就是来控制正确率的，经过测试一般设在20~35就差不多了

最后

./moso.py

或者

python moso.py

来运行他吧，之后你就可以挂着去干其他事情啦！