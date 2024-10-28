# 仓输入法(Hamster) 自用脚本
## DeepSeek
```javascript
// author: 叙白
// date: 2024-10-09
// name: DeepSeek.js
// 注意：请在脚本中的变量功能中添加 deepseek_key 变量，值为 DeepSeek 的 API Key
// 如果您使用转发平台的 API ，则值为转发平台的 API Key, 并且修改BASE_URL
// 此脚本仅兼容openai格式(openai, deepseek, kimi以及更多兼容openai格式的都可使用，温度需要根据各家ai自行调整)

// 依次为base_url, 默认模型，默认温度，不懂请勿修改
const BASE_URL = "https://api.deepseek.com/v1/chat/completions";
const DEFAULT_MODEL = "deepseek-chat";

// 不同任务类型的推荐温度值：代码生成/数学解题 0.0, 数据抽取/分析 1.0, 通用对话 1.3, 翻译 1.3, 创意类写作/诗歌创作 1.5
const DEFAULT_TEMPERATURE = 1.3;

async function deepseekDemo(question = "你好", options = {}) {
  const {
    model = DEFAULT_MODEL,
    temperature = DEFAULT_TEMPERATURE,
    isShortAnswer = !question.endsWith('-')  // 默认简短回答
  } = options;

  // 可自定义systemPrompt，在你的问题结尾后加-号，会自动帮你转短问
  const systemPrompt = `你是一位AI助手，能够回答的专业以及准确${isShortAnswer ? "，现在请尽量用一句话回答我的问题" : ""}`;

  const messages = [
    { role: "system", content: systemPrompt },
    { role: "user", content: question }
  ];

  try {
    const resp = await $http({
      url: BASE_URL,
      method: "post",
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${$deepseek_key}`,
      },
      body: { messages, model, temperature },
      timeout: 30,
    });

    const statusCode = resp.response.statusCode;
    if (statusCode !== 200) {
      throw new Error(`API请求失败: HTTP状态码 ${statusCode}`);
    }

    const parsedData = JSON.parse(resp.data);
    if (!parsedData.choices || parsedData.choices.length === 0) {
      throw new Error('API返回数据格式错误: 没有找到有效的回复');
    }

    return parsedData.choices[0].message?.content || "";
  } catch (error) {
    let errorMessage = '未知错误';
    if (error instanceof SyntaxError) {
      errorMessage = 'API返回的数据无法解析为JSON';
    } else if (error.message) {
      errorMessage = error.message;
    }
    $log(`DeepSeek API 错误: ${errorMessage}`);
    if (error.response) {
      $log(`响应详情: ${JSON.stringify(error.response)}`);
    }
    return `抱歉，发生了错误: ${errorMessage}`;
  }
}

async function output() {
  const question = $searchText || $pasteboardContent || "你好";
  return await deepseekDemo(question);
}
```
## Gemini
```js
// author: 叙白
// date: 2024-10-03
// name: Gemini.js
// 注意：请在脚本中的变量功能中添加 gemini_key 变量，值为 Gemini 的 API Key

const BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models";
const DEFAULT_MODEL = "gemini-1.5-flash";

async function geminiDemo(question = "你好", options = {}) {
  const {
    model = DEFAULT_MODEL,
    isShortAnswer = question.endsWith('-')
  } = options;

  const systemPrompt = `你是一位AI助手，能够回答的专业以及准确${isShortAnswer ? "，现在请尽量用一句话回答我的问题" : ""}`;

  const url = `${BASE_URL}/${model}:generateContent?key=${$gemini_key}`;
  const body = {
    'system_instruction': {
      'parts': {
        'text': systemPrompt
      }
    },
    'contents': {
      'parts': {
        'text': question
      }
    }
  };

  try {
    const resp = await $http({
      url,
      method: "post",
      header: {
        "Content-Type": "application/json"
      },
      body: body,
      timeout: 30,
    });

    const statusCode = resp.response.statusCode;
    if (statusCode !== 200) {
      throw new Error(`API请求失败: HTTP状态码 ${statusCode}`);
    }

    const parsedData = JSON.parse(resp.data);
    if (!parsedData.candidates || parsedData.candidates.length === 0) {
      throw new Error('API返回数据格式错误: 没有找到有效的回复');
    }

    return parsedData.candidates[0].content.parts[0].text || "";
  } catch (error) {
    let errorMessage = '未知错误';
    if (error instanceof SyntaxError) {
      errorMessage = 'API返回的数据无法解析为JSON';
    } else if (error.message) {
      errorMessage = error.message;
    }
    $log(`Gemini API 错误: ${errorMessage}`);
    if (error.response) {
      $log(`响应详情: ${JSON.stringify(error.response)}`);
    }
    return `抱歉，发生了错误: ${errorMessage}`;
  }
}

async function output() {
  const question = $searchText || $pasteboardContent || "你好-";
  return await geminiDemo(question);
}
```
