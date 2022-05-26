Cloud ESP32 e-Paper Board Host程序简明使用说明

1.安装必要库
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-tqdm
sudo apt-get install python3-numpy
sudo apt-get install python3-progressbar


2.程序
在当前目录下运行

sudo python3 ./examples/***inch_display_EPD

该程序会根据程序生成对应尺寸的图形和读取一张图片并发送给从机显示

示例：

如果使用4.2inch e-Paper Cloud Module
sudo python3 ./examples/4.2inch_display_EPD

如果使用2.13inch e-Paper Cloud Module
sudo python3 ./examples/2.13inch_display_EPD

注：以上程序连接和结束均会被记录在Histroy.txt中