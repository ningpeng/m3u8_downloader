m3u8_downloader
===============

m3u8 下载工具、模拟器
---------------
###依赖包安装
git clone https://github.com/globocom/m3u8.git
python setup.py install

###下载m3u8 url 为ts文件, 持续时间为1个小时
		example: ./hlsdownloader.py <m3u8_url> test.hls 3600

###监测一个m3u8 地址是否可用，持续时间为24小时
		example: ./hlsdownloader.py <m3u8_url> /dev/null 86400
