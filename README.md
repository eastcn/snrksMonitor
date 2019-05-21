# snrksMonitor
主要功能模块为：监控snkrs是否有上新（后续会加入对库存量的更新），为访问nike接口的IP池建立，以及后续有可能更新的抢购功能。

监控模块主要流程为：
爬取四个国区的数据-保存到数据库-再次爬取-进行比较-得出结果-进入休眠

数据库采用的是sqlite，因此也一并上传了。

# 2019-5-21更新
增加了一种推送方式，bark。目前只支持在IOS上使用。
在APPStore中下载 barK APP,获取自己设备的token。
在SnrksMonitor/new_ios_push.py文件的PushToIos.Push_list中加入自己的token即可。
