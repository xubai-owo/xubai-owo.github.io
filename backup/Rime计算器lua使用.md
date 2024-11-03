## 1. 准备文件
将 `calculator_translator.lua` 文件放入 Rime 目录下的 `lua/` 文件夹中。
[脚本链接](https://github.com/baopaau/rime-lua-collection/blob/master/calculator_translator.lua), 也可在仓输入法的QQ群内获取 704160594

## 2. 修改方案文件

### 2.1 配置 `engine/translators`
在方案文件（例如 `xxx.schema.yaml`）中的 `engine/translators` 下添加一行：

```yaml
- lua_translator@*calculator_translator
```

### 2.2 配置 `recognizer/patterns`
在 `recognizer/patterns` 下增加一行：

```yaml
expression: "^=.*$"
```
例如(仅为帮助理解的例子，关注最后一行即可)
```yaml
recognizer:
  import_preset: default
  patterns:
    punct: "^/([0-9]0?|[A-Za-z]+)$"
    # uppercase: "" #中文状态大写锁定直接上屏
    reverse_lookup: "^`[a-z]*'?$"
    easy_english: "^'[A-Z|a-z]*`?$"
    expression: "^=.*$"
```
### 2.3 使用补丁文件
> [!IMPORTANT]
> 注意: 若使用直接在方案文件(xxx.schema.yaml)中修改的方式，就不用看这个了!

如果需要使用补丁文件，可以创建 `xxx.custom.yaml` 文件（或修改已有文件），其中 `xxx` 对应方案文件名。内容如下：

```yaml
patch:
  engine/translators/+: [lua_translator@*calculator_translator]
  recognizer/patterns/expression: "^=.*$"
```

>[!TIP] 
> **注意：** 若已存在补丁文件，请勿重复粘贴 `patch` 部分。直接在已有文件中添加配置，保持与原文件缩进一致。

例如，若已有的custom文件内容是
```yaml
patch:
  translator/dictionary: tigress.extended
  menu/page_size: 9 
```
合并后为
```yaml
patch:
  engine/translators/+: [lua_translator@*calculator_translator]
  recognizer/patterns/expression: "^=.*$"
  translator/dictionary: tigress.extended
  menu/page_size: 9 
```