## 1. 准备文件
1. 将 [`calculator_translator.lua`](https://github.com/baopaau/rime-lua-collection/blob/master/calculator_translator.lua) 文件放入 `Hamster/Rime/lua` 文件夹中。
2. 也可以通过仓输入法的QQ群（群号：704160594）获取。

> [!Important]
>
> 修改方案文件和使用补丁文件二选一即可。

------

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
------

## 3. 使用补丁文件

如果你不想直接修改方案文件，可以采用补丁文件的方式，优点是不影响原方案的更新。

1. 创建 `xxx.custom.yaml` 文件（或修改已有文件），其中 `xxx` 对应方案文件名。(例如：你有方案文件名为`rime_ice.schema.yaml`， 新建的补丁文件就为`rime_ice.custom.yaml`)
2. 在补丁文件中添加如下内容：

```yaml
patch:
  engine/translators/+: [lua_translator@*calculator_translator]
  recognizer/patterns/expression: "^=.*$"
```

>[!TIP] 
>**注意：** 若已存在补丁文件，请勿重复粘贴 `patch` 部分。直接在已有文件中添加配置，保持与原文件缩进一致。
>
>
> 例如，若已有的custom文件内容是
>```yaml
>patch:
>      translator/dictionary: tigress.extended
>      menu/page_size: 9 
>```
>合并后为
>```yaml
>patch:
>      engine/translators/+: [lua_translator@*calculator_translator]
>      recognizer/patterns/expression: "^=.*$"
>      translator/dictionary: tigress.extended
>      menu/page_size: 9 
>```

## 4. 可能会遇到的问题

### 1. 按下`=`号后，直接上屏了，或者后续输入数字时也直接上屏

 - 如果用的是默认布局而不是皮肤，检查一下 键盘设置>数字九宫格 ，需要开启**数字键**、**左侧符号**、**右侧符号**由Rime处理。
 - 如果用的是键盘皮肤，需要检查一下用到的这些符号，对应的按键action是不是character，如果是symbol，需要改为character。
