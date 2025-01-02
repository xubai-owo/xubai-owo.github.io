import re
import os
import argparse
from pathlib import Path

# 上划按键行为和显示
swipeUpActionMap = {
    "q": {"action": '{ character: "1" }', "label": 'text: "1"'},
    "w": {"action": '{ character: "2" }', "label": 'text: "2"'},
    "e": {"action": '{ character: "3" }', "label": 'text: "3"'},
    "r": {"action": '{ character: "4" }', "label": 'text: "4"'},
    "t": {"action": '{ character: "5" }', "label": 'text: "5"'},
    "y": {"action": '{ character: "6" }', "label": 'text: "6"'},
    "u": {"action": '{ character: "7" }', "label": 'text: "7"'},
    "i": {"action": '{ character: "8" }', "label": 'text: "8"'},
    "o": {"action": '{ character: "9" }', "label": 'text: "9"'},
    "p": {"action": '{ character: "0" }', "label": 'text: "0"'},
    "a": {"action": '{ character: "`" }', "label": 'text: "`"'},
    "s": {"action": '{ character: "-" }', "label": 'text: "-"'},
    "d": {"action": '{ character: "=" }', "label": 'text: "="'},
    "f": {"action": '{ character: "[" }', "label": 'text: "["'},
    "g": {"action": '{ character: "]" }', "label": 'text: "]"'},
    "h": {"action": '{ character: "\\\\" }', "label": 'text: "\\\\"'},
    "j": {"action": '{ character: "/" }', "label": 'text: "/"'},
    "k": {"action": '{ character: ";" }', "label": 'text: ";"'},
    "l": {"action": "{ character: \"'\" }", "label": "text: \"'\""},
    "z": {"action": 'tab', "label": 'text: "⇥"'},
    "x": {"action": '{ symbol: "「" }', "label": 'text: "「"'},
    "c": {"action": '{ symbol: "」" }', "label": 'text: "」"'},
    "v": {"action": '{ character: "<" }', "label": 'text: "<"'},
    "b": {"action": '{ character: ">" }', "label": 'text: ">"'},
    "n": {"action": '{ character: "," }', "label": 'text: ","'},
    "m": {"action": '{ character: "." }', "label": 'text: "."'}
}

# 下划按键行为和显示
swipeDownActionMap = {
    #二十六键
    "q": {"action": '{ character: "!" }', "label": 'text: "!"'},
    "w": {"action": '{ character: "@" }', "label": 'text: "@"'},
    "e": {"action": '{ character: "#" }', "label": 'text: "#"'},
    "r": {"action": '{ character: "$" }', "label": 'text: "$"'},
    "t": {"action": '{ character: "%" }', "label": 'text: "%"'},
    "y": {"action": '{ character: "^" }', "label": 'text: "^"'},
    "u": {"action": '{ character: "&" }', "label": 'text: "&"'},
    "i": {"action": '{ character: "*" }', "label": 'text: "*"'},
    "o": {"action": '{ character: "(" }', "label": 'text: "("'},
    "p": {"action": '{ character: ")" }', "label": 'text: ")"'},
    "a": {"action": '{ character: "~" }', "label": 'text: "~"'},
    "s": {"action": '{ character: "_" }', "label": 'text: "_"'},
    "d": {"action": '{ character: "+" }', "label": 'text: "+"'},
    "f": {"action": '{ character: "{" }', "label": 'text: "{"'},
    "g": {"action": '{ character: "}" }', "label": 'text: "}"'},
    "h": {"action": '{ character: "|" }', "label": 'text: "|"'},
    "j": {"action": '{ character: "?" }', "label": 'text: "?"'},
    "k": {"action": '{ character: ":" }', "label": 'text: ":"'},
    "l": {"action": '{ character: \'"\' }', "label": 'text: \'"\''},
    "z": {"action": '{ shortcutCommand: "#行首" }', "label": 'text: "行首"'},
    "x": {"action": '{ shortcutCommand: "#行尾" }', "label": 'text: "行尾"'},
    "c": {"action": '{ symbol: "·" }', "label": 'text: "·"'},
    "v": {"action": '{ symbol: "……" }', "label": 'text: "…"'},
    "b": {"action": '{ shortcutCommand: "#复制" }', "label": 'text: "复制"'},
    "n": {"action": '{ shortcutCommand: "#粘贴" }', "label": 'text: "粘贴"'},
    "m": {"action": '{ shortcutCommand: "#selectText" }', "label": 'text: "全选"'},
    # 九宫格用1-9
    "1": {"action": '{ shortcutCommand: "#重输" }', "label": 'text: "重输"'},
    "2": {"action": '{ shortcutCommand: "#行首" }', "label": 'text: "行首"'},
    "3": {"action": '{ shortcutCommand: "#行尾" }', "label": 'text: "行尾"'},
    "4": {"action": '{ shortcutCommand: "#selectText" }', "label": 'text: "全选"'},
    "5": {"action": '{ shortcutCommand: "#复制" }', "label": 'text: "复制"'},
    "6": {"action": '{ shortcutCommand: "#粘贴" }', "label": 'text: "粘贴"'},
    "7": {"action": '{ shortcutCommand: "#右手" }', "label": 'text: "右手"'},
    "8": {"action": '{ shortcutCommand: "#剪切" }', "label": 'text: "剪切"'},
    "9": {"action": '{ shortcutCommand: "#换行" }', "label": 'text: "换行"'}
}

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def get_new_swipe_action(button_name, orientation):
    if orientation == "up":
        if button_name in swipeUpActionMap:
            return swipeUpActionMap[button_name]["action"]
        return ""
    if button_name in swipeDownActionMap:
        return swipeDownActionMap[button_name]["action"]
    return ""
def get_new_swipe_label(button_name, orientation):
    if orientation == "up":
        if button_name in swipeUpActionMap:
            return swipeUpActionMap[button_name]["label"]
        return None
    if button_name in swipeDownActionMap:
        return swipeDownActionMap[button_name]["label"]
    return None
 
def pinyin26(file_content):
    def update_swipe_label(line, pattern, direction, file_content, count):
        if pattern.match(line):  # 匹配到按钮划动样式定义行
            button_name = line.split(':')[0]  # 提取按钮名称
            new_label = get_new_swipe_label(button_name[0], direction)
            if new_label is not None:
                file_content[count + 1] = f"  {new_label}\n"

    # 匹配正则
    button_pattern = re.compile(r'[a-z]Button:$')
    button_up_label_pattern = re.compile(r'[a-z]ButtonUpForegroundStyle:$')
    button_down_label_pattern = re.compile(r'[a-z]ButtonDownForegroundStyle:$')

    count = 0
    
    for line in file_content:
        # 替换action
        if button_pattern.match(line): # 匹配到按钮定义行
            button_name = line.split(':')[0] # 提取按钮名称
            # 从count开始，向下查找swipeUpAction
            for i in range(count, len(file_content)):
                # 替换上划行为
                if 'swipeUpAction' in file_content[i]:
                    new_action = get_new_swipe_action(button_name[0], "up")
                    file_content[i] = f"  swipeUpAction: {new_action}\n"
                # 替换下划行为
                if 'swipeDownAction' in file_content[i]:
                    new_action = get_new_swipe_action(button_name[0], "down")
                    file_content[i] = f"  swipeDownAction: {new_action}\n"
                    break
        # 替换划动显示
        if button_up_label_pattern.match(line) or button_down_label_pattern.match(line): # 匹配到按钮划动样式定义行
            update_swipe_label(line, button_up_label_pattern, "up", file_content, count)
            update_swipe_label(line, button_down_label_pattern, "down", file_content, count)
        count += 1
    return file_content

def pinyin9(file_content):
    button_pattern = re.compile(r'number[0-9]Button:$')
    button_down_pattern = re.compile(r'number[0-9]DownButtonForegroundStyle:$')

    count = 0
    
    for line in file_content:
        # 替换上下划action
        if button_pattern.match(line): # 匹配到按钮定义行
            button_name = line.split(':')[0] # 提取按钮名称
            # for i in range(count, len(file_content)):
            #     if 'swipeUpAction' in file_content[i]:
            #         new_action = get_new_swipe_action(button_name[6], "up")
            #         file_content[i] = f"  swipeDownAction: {new_action}\n"
            #         break  # 只要找到了swipeUpAction，就退出循环
            for i in range(count, len(file_content)):
                if 'swipeDownAction' in file_content[i]:
                    new_action = get_new_swipe_action(button_name[6], "down")
                    file_content[i] = f"  swipeDownAction: {new_action}\n"
                    break  # 只要找到了swipeUpAction，就退出循环
            
        # 替换下划划动显示
        if button_down_pattern.match(line): # 匹配到按钮下划样式定义行
            button_name = line.split(':')[0] # 提取按钮名称
            new_label = get_new_swipe_label(button_name[6], "down")
            file_content[count+1] = f"  {new_label}\n"
        count += 1
    return file_content


def save_file(file_path, file_content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(file_content)


def process(file_path):
    # 递归遍历file_path目录下所有文件, 对指定文件进行处理，并写入原文件
    process_files = [
        "pinyin_26_portrait.yaml", 
        "alphabetic_26_portrait.yaml", 
        "pinyin_9_portrait.yaml",
        "alphabetic_9_portrait.yaml"
    ]
    for root, _, files in os.walk(file_path):
        for file in files:
            if file in process_files:
                print(f"处理文件: {file}")
                file_path = os.path.join(root, file)
                file_content = load_file(file_path)
                if "pinyin_9_portrait.yaml" in file_path:
                    new_file_content = pinyin9(file_content)
                else:
                    new_file_content = pinyin26(file_content)
                save_file(file_path, new_file_content)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="处理源目录文件")
    parser.add_argument("source", type=Path, help="源目录路径")
    args = parser.parse_args()   
    process(args.source)
