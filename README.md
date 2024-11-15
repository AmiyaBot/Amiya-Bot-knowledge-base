# AmiyaBot AI 知识库

适用于 [百度智能云千帆AppBuilder](https://qianfan.cloud.baidu.com/appbuilder/) 的明日方舟游戏知识库。可一键自动创建知识库和增量更新知识库文件。

## 配置

1. 在 `config/gamedata.json`
   里配置 [gamedata](https://github.com/Kengxxiao/ArknightsGameData/tree/master/zh_CN/gamedata)
   的文件路径。
2. （可选）在 `config/baidu.json` 里配置千帆AppBuilder的 [密钥](https://console.bce.baidu.com/ai_apaas/secretKey)
   、知识库的名称与描述，以及切片的最大长度。

## 生成

```base
pip install -r requirements.txt
run.bat
```

随后在 `dist` 目录内输出知识库文件，若配置了千帆AppBuilder，则会自动上传到知识库。

> 重复运行时，会检查知识库文件的状态增量更新知识库文件。
