<div align="center">
<h1>DNre-Build</h1>
DN怀旧服配装模拟器<br><br>

![DNre-Build](https://github.com/aaron-lii/DNre-Build/raw/main/data/logo2.ico)
</div>

## 简介
1. 勾选配装，能计算出面板数值
2. 勾选不同buff，能计算副本内加完buff后的面板
3. 设置技能数值和BOSS，能计算当前配装战斗力和生存力
4. 根据不同BOSS，能计算出三属性纹章和石板继续堆某个属性的收益率


## windows整合包使用说明
1. 下载并解压后，直接运行`run.bat`
2. 正常情况下会自动打开配装器网页，没有的话就浏览器手动打开网址`http://127.0.0.1:7866`
3. 使用过程中请不要关闭命令行窗口

## 开发者使用说明
1. 安装依赖`pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`
2. 运行`python app.py`，正常情况下会自动打开配装器网页，没有的话就浏览器手动打开网址`http://127.0.0.1:7866`

## TODO
1. 回蓝眩晕硬直面板计算异常
2. 某些职业输出结构复杂，战斗力衡量标准需要再思考一下
3. 覆盖率非全程的职业buff加入计算

## 维护数据
+ `boss.json`
+ `dps_type.json`
+ `skill.json`
+ `skin.json`
+ `state_rate.json`
+ `surplus.json`

## 感谢技术支持
+ DN聚集地-阿笑
+ [DN聚集地](https://dngamer.site/)