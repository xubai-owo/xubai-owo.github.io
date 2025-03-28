## DeepSeek
> [!TIP]
> 请在脚本中的变量功能中添加 deepseek_key 变量，值为 DeepSeek 的 API Key
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
> [!TIP]
> 请在脚本中的变量功能中添加 gemini_key 变量，值为 Gemini 的 API Key
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
## Base64编解码
> [!TIP]
> E需要编码的字符串/D需要解码的字符串
```js
// author: 叙白
// name: base64编码解码.js
// date: 2024-09-25
// 使用：E需要编码的字符串/D需要解码的字符串

function base64Encode(str) {
  // 将字符串转换为 UTF-8 编码
  const utf8Bytes = unescape(encodeURIComponent(str));
  let output = '';
  let buffer = 0;
  let bitsCollected = 0;

  for (let byte of utf8Bytes) {
    buffer = (buffer << 8) | byte.charCodeAt(0);
    bitsCollected += 8;

    while (bitsCollected >= 6) {
      bitsCollected -= 6;
      output += 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='[(buffer >> bitsCollected) & 0x3F];
    }
  }


  if (bitsCollected > 0) {
    buffer <<= (6 - bitsCollected);
    output += 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='[(buffer & 0x3F)];
    output += '='; // 添加填充
  }

  return output;
}

function base64Decode(str) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
  let output = '';
  let buffer = 0;
  let bitsCollected = 0;

  for (let char of str) {
    if (char === '=') break;
    const charIndex = chars.indexOf(char);
    if (charIndex === -1) continue; // 忽略非法字符

    buffer = (buffer << 6) | charIndex;
    bitsCollected += 6;

    while (bitsCollected >= 8) {
      bitsCollected -= 8;
      output += String.fromCharCode((buffer >> bitsCollected) & 0xFF);
    }
  }

  // 将解码后的字节转换回 UTF-8
  return decodeURIComponent(escape(output));
}

async function output() {
  const text = $searchText || $pasteboardContent
  if (!text) {
    return "请输入内容!";
  }
  if (text[0] === "E") {
    return base64Encode(text.slice(1));;
  } else if (text[0] === "D") {
    return base64Decode(text.slice(1));
  } else {
    return "请输入正确的指令";
  }
}
```
## Deeplx
> [!TIP]
> 需添加变量deeplx_key
```js
// author: 叙白
// date: 2024-09-25
// name: Deeplx.js
// 注意: 需添加变量deeplx_key
// 使用： 要翻译成英文或中文，在翻译文本前加“中/英”， 例： 中我要回家，将会翻译成英文

async function output() {
  const text = $searchText || $pasteboardContent;
  if (!text) return null; // 检查输入是否为空

  const langMap = {
    "中": "ZH",
    "英": "EN"
  };

  const target = langMap[text[0]]; // 根据首字符映射语言
  if (!target) return null; // 如果没有匹配到对应语言，直接返回

  const payload = {
    text: text.slice(1),
    source_lang: "auto",
    target_lang: target
  };

  try {
    const response = await $http({
      url: `https://api.deeplx.org/${$deeplx_key}/translate`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      body: payload,
    });

    if (response.response.statusCode !== 200) {
      return "请求失败";
    }

    return JSON.parse(response.data).data;
  } catch (error) {
    $log(error);
    return null;
  }
}
```
### Deeplx中英自动翻译
```js
// author: 叙白
// date: 2024-09-28
// name: Deeplx中外互译.js
// 注意: 需添加变量deeplx_key
// 使用：输入中文自动翻译成英文，输入非中文自动翻译成中文

async function output() {
  const text = $searchText || $pasteboardContent || "测试文本";
  if (!text) return "请输入要翻译的文本"; // 检查输入是否为空


  let target = await detectLang(text); // 自动检测语言并翻译
  let translatedText = await translate(text, target); // 翻译文本
  return translatedText;
  
}

async function detectLang(text) {
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=auto&dt=t&q=${encodeURIComponent(text)}`;
		// 第一次调用 googleTranslate 函数，检测并翻译文本
    const resp = await $http({
      url,
      header: {"Content-Type": "application/json"}
      });

    if (resp.response.statusCode !== 200) {
      return "翻译失败";
    }

    const jsonDict = JSON.parse(resp.data);
    const detectedLang = jsonDict[2]; // 这个字段包含检测到的源语言

    // 根据检测到的源语言决定目标语言
    let targetLang = detectedLang === "zh-CN" ? "EN" : "ZH";
    return targetLang;
  } catch (error) {
    throw new Error(error);
  }
}

async function translate(text, target) {
  const payload = {
    text: text,
    source_lang: "auto",
    target_lang: target
  };

  try {
    const response = await $http({
      url: `https://api.deeplx.org/${$deeplx_key}/translate`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      body: payload,
    });

    if (response.response.statusCode !== 200) {
      return "请求失败";
    }
    $log(response.data);
    return JSON.parse(response.data).data;
  } catch (error) {
    $log(error);
    return null;
  }
}
```
## 每日油价
```js
// name: 每日油价.js
// data: 2024-10-18
// author: 叙白
// desc: 自行设置你需要的省份

async function output() {
	// 省份名自行替换
	return await getOilPrice("广东省");
}

async function getOilPrice(regionName) {
	const url = "https://v2.api-m.com/api/oilPrice"
	const {data} = await $http({url: url});
	const jsonData = JSON.parse(data);
	const region = jsonData.data.filter(item => item.regionName === regionName)[0];
	const prices = [
  `92汽油: ${region.n92}元`,
  `95汽油: ${region.n95}元`,
  `98汽油: ${region.n98}元`,
  `0号柴油: ${region.n0}元`
];
  return prices;
}
```
## 汇率
```js
// author: 叙白
// name: 汇率.js
// data: 2024-09-26
// 使用: 不在输入框中输入数字，直接点击按钮，则默认转换为 1 基准货币 兑 其他货币汇率。
// 输入框中输入数字，则转换为输入数字 基准货币 兑 其他货币汇率。
const currencyNames = {
  cny: ["人民币", "🇨🇳"],
  usd: ["美元", "🇺🇸"],
  hkd: ["港币", "🇭🇰"],
  jpy: ["日元", "🇯🇵"],
  eur: ["欧元", "🇪🇺"],
  gbp: ["英镑", "🇬🇧"],
};
let defaultBaseCurrency = "cny"; // 全局设置基准货币

// 异步函数来处理汇率转换
async function output() {
  let text = $searchText;
  const precision = 4; // 保留小数
  
  // 检测并提取输入的数字和基准货币
  const { amount, baseCurrency } = extractAmountAndCurrency(text) || { amount: 1, baseCurrency: defaultBaseCurrency };

  const exchangeData = await getCurrencyData(baseCurrency);

  const result = formatExchangeRates(exchangeData, baseCurrency, amount, precision);
  return result;
}

function extractAmountAndCurrency(text) {
  if (!text) return { amount: 1, baseCurrency: defaultBaseCurrency }; // 默认值处理

  // 匹配数字（可以是小数）和货币代码或名称
  const regex = /(\d+(\.\d+)?)\s*([a-zA-Z]+|[\u4e00-\u9fa5]+)?/;
  const match = text.match(regex);

  if (match) {
    const amount = parseFloat(match[1]);
    const currencyText = match[3]?.toLowerCase();

    // 如果匹配到货币种类，返回对应的货币，否则使用默认基准货币
    if (currencyText) {
      for (const [currency, [name]] of Object.entries(currencyNames)) {
        if (currency === currencyText || name.includes(currencyText)) {
          return { amount, baseCurrency: currency };
        }
      }
    }

    // 没有匹配到货币时，使用全局默认的基准货币
    return { amount, baseCurrency: defaultBaseCurrency };
  }

  return { amount: 1, baseCurrency: defaultBaseCurrency };
}

async function getCurrencyData(baseCurrency) {
  const url = `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/${baseCurrency}.json`;
  try {
      const resp = await $http({ url: url, method: 'GET' });
      const jsonData = JSON.parse(resp.data);
      return jsonData;
  } catch (error) {
      $log(error);
      return null;
  }
}

// 格式化汇率转换的逻辑，增加 amount 参数
function formatExchangeRates(data, baseCurrency, amount = 1, precision = 4) {
  const result = [];

  // 获取基准货币对其他货币的汇率
  const baseRates = data[baseCurrency];

  if (!baseRates || !currencyNames[baseCurrency]) {
    return `基准货币 ${baseCurrency} 不存在或无效`;
  }

  const [baseCurrencyName, baseFlag] = currencyNames[baseCurrency];

  // 遍历本地 currencyNames
  for (const [currency, [foreignCurrencyName, foreignFlag]] of Object.entries(currencyNames)) {
    if (currency === baseCurrency) {
      continue; // 跳过基准货币
    }

    const rate = baseRates[currency];
    if (rate) {
      const convertedAmount = (amount * rate).toFixed(precision);
      result.push(`${amount} ${baseCurrencyName} ${baseFlag} 兑 ${convertedAmount} ${foreignCurrencyName} ${foreignFlag}`);
    }
  }
  return result;
}
```
## 热搜
```js
// name: 热搜.js
// date: 2024-10-17
// author: 叙白
// desc: 来自龙珠api

async function output() {
	// zhihu(知乎热榜)weibo(微博热搜) baidu(百度热点)history(历史上的今天)bilihot(哔哩哔哩热搜)biliall(哔哩哔哩全站日榜)douyin(抖音热搜)
	// type后替换上面这些获取不同的热搜
	const url = "https://www.hhlqilongzhu.cn/api/rs_juhe.php?type=douyin"
	return getTrending(url);

}

async function getTrending(url) {
	const {data} = await $http({url: url});
	const dataList = JSON.parse(data).data;
	
	const titles = dataList.map(item => item.title);
	return titles;
}
```
## 谷歌翻译
```js
// author: 叙白
// name: 谷歌翻译.js
// date: 2024-09-25
// 使用： 要翻译成英文或中文，在翻译文本前加“中/英”， 例： 中我要回家，将会翻译成英文 

async function googleTranslate(target, text) {
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${target}&dt=t&q=${encodeURIComponent(text)}`;
    const resp = await $http({
      url,
      header: {
        "Content-Type": "application/json",
      }
    });

    if (resp.response.statusCode!== 200) {
      return "翻译失败";
    }
    const jsonDict = JSON.parse(resp.data);
    const translatedText = jsonDict[0].map(item => item[0]).join('');
    return translatedText;

  } catch (error) {
    $log(error);
  }
}

async function output() {
  var text = $searchText || $pasteboardContent || "d l";
  if (!text) {
    return "请输入要翻译的文本";
  }
  let target = "";
  const languageMap = {
    "中": "zh-CN",
    "英": "en",
    "韩": "ko",
    "日": "ja"
    // 添加更多语言映射
  };
  target = languageMap[text[0]] || "zh";
  text = text.slice(1);
  const translatedText = await googleTranslate(target, text);
  return translatedText;
}
```

### 谷歌中英自动翻译
```js
// author: 叙白
// name: 谷歌中英互译.js
// date: 2024-09-27

async function googleTranslate(text) {
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=auto&dt=t&q=${encodeURIComponent(text)}`;
		// 第一次调用 googleTranslate 函数，检测并翻译文本
    const resp = await $http({
      url,
      header: {"Content-Type": "application/json"}
      });

    if (resp.response.statusCode !== 200) {
      return "翻译失败";
    }

    const jsonDict = JSON.parse(resp.data);
    const detectedLang = jsonDict[2]; // 这个字段包含检测到的源语言

    // 根据检测到的源语言决定目标语言
    let targetLang = detectedLang === "zh-CN" ? "en" : "zh-CN";

    // 进行第二次翻译，这次使用目标语言
    const urlWithTarget = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${detectedLang}&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
    const respWithTarget = await $http({
      url: urlWithTarget,
      header: {
        "Content-Type": "application/json",
      }
    });

    if (respWithTarget.response.statusCode !== 200) {
      return "翻译失败";
    }

    const translatedText = JSON.parse(respWithTarget.data)[0].map(item => item[0]).join('');
    return translatedText;

  } catch (error) {
    $log(error);
    return "翻译过程中出现错误";
  }
}

async function output() {
  var text = $searchText || $pasteboardContent || "你好";
  if (!text) {
    return "请输入要翻译的文本";
  }
  
  const translatedText = await googleTranslate(text);
  return translatedText;
}
```

## 每日新闻
```js
// name: 新闻.js
// date: 2024-11-04
// author: 叙白

async function output() {
	let url = "http://api.suxun.site/api/sixs?type=json";
	return await getData(url);
	
}

async function getData(url) {
	const { data } = await $http({url: url});
	const jsonData = JSON.parse(data);
	let news = jsonData.news;
	return news;
}
```

## 智谱ai翻译
```js
// author: 叙白
// date: 2025-01-18
// name: BigModelTranslator.js
// 注意：请在脚本中的变量功能中添加 bigmodel_key 变量，值为 BigModel 的 API Key

const BASE_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions";
const DEFAULT_MODEL = "glm-4-flash";
const DEFAULT_TEMPERATURE = 0.1;

/**
 * 主函数，用于处理输入并输出翻译结果
 */
async function output() {
  var text = $searchText || $pasteboardContent;
  if (!text) {
    return "";
  }
  return await bigModelTranslate(text);
}

/**
 * 调用 BigModel 翻译 API
 * @param {string} text - 需要翻译的文本
 * @returns {Promise<string>} - 翻译后的文本
 */
async function bigModelTranslate(text) {
  const messages = [
    {
      role: "system",
      content: "You are a professional, authentic machine translation engine.",
    },
    {
      role: "user",
      content: `; 把下一行文本作为纯文本输入，对该文本进行中文和外语的互译,仅输出翻译。如果某些内容无需翻译（如专有名词、代码等），则保持原文不变。 不要解释，输入文本:\n${text}`,
    },
  ];

  try {
    const response = await $http({
      url: BASE_URL,
      method: "POST",
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${$bigmodel_key}`,
      },
      body: {
        messages,
        model: DEFAULT_MODEL,
        temperature: DEFAULT_TEMPERATURE,
        top_p: 0.1,
        max_tokens: 2048,
      },
      timeout: 30,
    });

    if (response.response.statusCode !== 200) {
      throw new Error(`API请求失败: HTTP状态码 ${response.response.statusCode}`);
    }

    const responseData = JSON.parse(response.data);
    if (!responseData.choices || responseData.choices.length === 0) {
      throw new Error("API返回数据格式错误: 没有找到有效的回复");
    }

    // 返回翻译后的内容
    return responseData.choices[0].message?.content || "";
  } catch (error) {
    const errorMessage =
      error instanceof SyntaxError
        ? "API返回的数据无法解析为JSON"
        : error.message || "未知错误";
    $log(`BigModel API 错误: ${errorMessage}`);
    if (error.response) {
      $log(`响应详情: ${JSON.stringify(error.response)}`);
    }
    return `抱歉，发生了错误: ${errorMessage}`;
  }
}
```