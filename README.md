<div align="center">
<h1>DNre-Build</h1>
DN怀旧服配装模拟器<br><br>

![DNre-Build](https://github.com/aaron-lii/DNre-Build/raw/main/data/logo2.ico)
</div>

## 项目简介

这是一个面向 DN 怀旧服的配装模拟器，当前主要用于：

1. 计算角色配装后的基础面板
2. 计算副本内叠加常用 buff 后的面板
3. 根据技能构成和目标 BOSS 估算战斗力与生存力
4. 分析纹章、石板等属性替换后的收益

当前版本已经覆盖 70 级相关内容，包括：

1. 70 级装备、首饰、卡片、纹章、时装等数据
2. 70 级远征队纹章
3. 70 级试炼地狱 BOSS
4. 致命伤害面板与收益计算
5. 刺客职业与相关 buff

## 说明

这个仓库现在公开给玩家一起维护。

我自己已经不太常玩游戏了，所以：

1. 游戏内后续更新的数值、词条、技能改动，可能无法第一时间同步
2. 某些职业的实战算法、覆盖率、特殊机制，可能仍然需要玩家实测修正
3. 如果你发现面板、收益、BOSS 属性、技能效果和游戏内不一致，欢迎直接提 issue 或提交 PR

如果你能提供以下内容，维护会快很多：

1. 游戏内面板截图
2. 技能说明或道具说明截图
3. 明确的角色等级、职业、装备、buff 条件
4. 你认为正确的计算结果或对照结果

## 本地运行

1. 安装依赖

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

2. 启动配装器

```bash
python app.py
```

3. 正常情况下会自动打开浏览器；如果没有自动打开，可手动访问：

```text
http://127.0.0.1:7866
```

## 目录说明

- `app.py`
  配装器入口
- `src/`
  核心计算逻辑
- `gradio_ui/`
  页面与交互
- `data/`
  运行时使用的数据文件

## 主要维护数据

运行时直接依赖的主要数据包括：

- `data/boss.json`
- `data/dps_type.json`
- `data/skill.json`
- `data/skin.json`
- `data/state_rate.json`
- `data/surplus.json`
- `data/player_base.json`
- `data/player_common_level.json`
- `data/glyph.json`
- `data/glyph2.json`
- `data/rune.json`
- `data/card.json`
- `data/equipment_base.json`
- `data/equipment_group.json`
- `data/equipment_grade.json`
- `data/equipment_suffix.json`
- `data/jewelry.json`

## 当前已知问题

1. 回蓝、眩晕、硬直相关面板仍有继续核对空间
2. 某些职业输出结构复杂，战斗力衡量标准仍然是近似模型
3. 覆盖率并非全程的职业 buff 还没有完整建模
4. 一些新增词条或特殊机制，仍需要更多玩家实测校验

## 协作建议

如果你准备提交 PR，建议尽量把修改分成以下几类之一：

1. 纯数据修正
2. 面板/收益公式修正
3. 新职业 / 新词条 / 新 BOSS 支持
4. UI 和交互优化

如果改动涉及算法，请尽量在 PR 描述里写清楚：

1. 游戏内依据
2. 计算口径
3. 测试样例

## 感谢

- DN聚集地-阿笑
- [DN聚集地](https://dngamer.site/)
