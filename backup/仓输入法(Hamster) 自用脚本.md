## BigModelTranslator.js

```javascript
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

## DeepSeek.js

```javascript
// author: 叙白
// date: 2025-01-19
// name: DeepSeek.js
// 注意：请在脚本中的变量功能中添加 deepseek_key 变量，值为 DeepSeek 的 API Key
// 如果您使用转发平台的 API ，则值为转发平台的 API Key, 并且修改 BASE_URL
// 此脚本仅兼容 OpenAI 格式 (openai, deepseek, kimi 以及更多兼容 OpenAI 格式的都可使用，温度需要根据各家 AI 自行调整)

const BASE_URL = "https://api.deepseek.com/v1/chat/completions";
const DEFAULT_MODEL = "deepseek-chat";
const DEFAULT_TEMPERATURE = 1.3; // 通用对话推荐温度

async function deepseekDemo(question = "你好", options = {}) {
  const {
    model = DEFAULT_MODEL,
    temperature = DEFAULT_TEMPERATURE,
    isShortAnswer = !question.endsWith('-')  // 默认简短回答
  } = options;

  const systemPrompt = `你是一位AI助手，能够回答的专业以及准确${isShortAnswer ? "，现在请尽量用一句话回答我的问题" : ""}`;

  const messages = [
    { role: "system", content: systemPrompt },
    { role: "user", content: question }
  ];

  try {
    const response = await $http({
      url: BASE_URL,
      method: "POST",
      header: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${$deepseek_key}`,
      },
      body: { messages, model, temperature },
      timeout: 30,
    });

    // 检查 HTTP 状态码
    if (response.response.statusCode !== 200) {
      const errorMessage = `API请求失败: HTTP状态码 ${response.response.statusCode}, 响应数据: ${response.data}`;
      $log(`DeepSeek API 错误: ${errorMessage}`);
      return `抱歉，发生了错误: ${errorMessage}`;
    }

    // 解析响应数据
    let responseData;
    try {
      responseData = JSON.parse(response.data);
    } catch (parseError) {
      const errorMessage = `API返回的数据无法解析为JSON: ${response.data}`;
      $log(`DeepSeek API 错误: ${errorMessage}`);
      return `抱歉，发生了错误: ${errorMessage}`;
    }

    // 检查响应数据格式
    if (!responseData.choices || responseData.choices.length === 0) {
      const errorMessage = `API返回数据格式错误: 没有找到有效的回复, 完整响应: ${JSON.stringify(responseData)}`;
      $log(`DeepSeek API 错误: ${errorMessage}`);
      return `抱歉，发生了错误: ${errorMessage}`;
    }

    return responseData.choices[0].message?.content || "";
  } catch (error) {
    // 捕获其他未知错误
    const errorMessage = error.message || '未知错误';
    $log(`DeepSeek API 错误: ${errorMessage}`);
    if (error.response) {
      $log(`响应详情: ${JSON.stringify(error.response)}`);
    }
    return `抱歉，发生了错误: ${errorMessage}`;
  }
}

async function output() {
  // 优先使用 $searchText，如果没有则使用 $pasteboardContent，最后使用默认值 "你好"
  const question = $searchText || $pasteboardContent || "你好";
  return await deepseekDemo(question);
}
```

## Deeplx.js

```javascript
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

## Deeplx中外互译.js

```javascript
// author: 叙白
// date: 2024-09-28
// name: Deeplx中外互译.js
// 注意: 需添加变量deeplx_key
// 使用： 要翻译成英文或中文，在翻译文本前加“中/英”， 例： 中我要回家，将会翻译成英文

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

## Gemini.js

```javascript
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

## Unicode.js

```javascript
// author: 叙白
// name: Unicode.js
// date: 2024-09-26

async function getUnicodeWithCharacter(str) {
    let unicodeArray = [];
    for (let i = 0; i < str.length; i++) {
        let char = str[i];
        let codePoint = str.codePointAt(i);
        
        // Skip the next code unit if this character is a high surrogate
        if (codePoint > 0xFFFF) {
            i++;
        }
        
        let unicode = char + ': U+' + codePoint.toString(16).toUpperCase();
        unicodeArray.push(unicode);
    }
    return unicodeArray.join('\n');
}

async function output() {
  const text = $searchText || $pasteboardContent; 
  const result = await getUnicodeWithCharacter(text);
  return result;
}
```

## base64编码解码.js

```javascript
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

## getScript.js

```javascript
// author: 叙白
// name: getScript.js
// date: 2024-09-26

function toRawGitHubLink(url) {
    if (url.includes('github.com') && url.includes('/blob/')) {
        return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/');
    }
    return url;
}

async function output() {
    const url = $searchText || $pasteboardContent;
    if (!url) {
        return "请输入url";
    }
    
    const processedUrl = toRawGitHubLink(url);

    try {
        const { data } = await $http({ url: processedUrl });
        return data;
    } catch (error) {
        $log(error);
        return "未知错误";
    }
}
```

## 发病语录.js

```javascript
// name: 发病语录.js
// date: 2024-10-18
// desc: OI api
// author: 叙白

async function output() {
	const url = "https://oiapi.net/API/SickL";
	return getMessage(url);
}  

async function getMessage(url) {
	const {data} = await $http({url: url});
	return JSON.parse(data).message;
}
```

## 多合一.js

```javascript
// name: 多合一.js

async function output() {
  try {
    // 使用 Promise.all 并行执行所有异步函数
    const results = await Promise.all([
      tiangou(),
      yiyan(),
      yulu(),
      fkxqs(),
      dujitang(),
      tapped()
    ]);

    // 遍历结果并输出
    let resulList = [];
    results.forEach((result, index) => {
      resulList.push(result);
    });

    return resulList;
  } catch (error) {
    $log(error);
    throw error;
  }
}

async function tiangou() {
  let tg = await $http({
    method: "GET",
    url: "https://api.oick.cn/dog/api.php",
    header: {
      site: "https://api.oick.cn"
    }
  });
  return tg.data;
}

async function yiyan() {
  let yy = await $http({
    method: "GET",
    url: "https://v1.hitokoto.cn/?c=f&encode=text",
    header: {
      site: "www.shadiao.app"
    }
  });
  return yy.data;
}

//社会人
async function yulu(){
  let tw = await $http({url: "https://api.oick.cn/yulu/api.php"});
  return tw.data;
};

//疯狂星期四
async function fkxqs() {
  let aa = await $http({
    method: "GET",
    url: "https://api.shadiao.pro/kfc",});
  
  return JSON.parse(aa.data).data.text;
};

//毒鸡汤
async function dujitang() {
  let aa = await $http({
    method: "GET",
    url: "https://api.shadiao.pro/du",});
  return JSON.parse(aa.data).data.text;
};

//骂人
async function tapped() {
  let aa = await $http({
    method: "GET",
    url: "https://yyapi.a1aa.cn/api.php?level=max",});
    return aa.data;
};
```

## 字符串转utf8数组.js

```javascript
// name: 字符串转utf8数组.js
// 工具类函数

function stringToUTF8Bytes(str) {
    const utf8 = [];
    for (let i = 0; i < str.length; i++) {
        let charCode = str.charCodeAt(i);
        if (charCode < 0x80) {
            utf8.push(charCode);
        } else if (charCode < 0x800) {
            utf8.push(0xc0 | (charCode >> 6), 0x80 | (charCode & 0x3f));
        } else if (charCode < 0x10000) {
            utf8.push(0xe0 | (charCode >> 12), 0x80 | ((charCode >> 6) & 0x3f), 0x80 | (charCode & 0x3f));
        } else {
            utf8.push(
                0xf0 | (charCode >> 18),
                0x80 | ((charCode >> 12) & 0x3f),
                0x80 | ((charCode >> 6) & 0x3f),
                0x80 | (charCode & 0x3f)
            );
        }
    }
    return utf8;
}

async function output(){
	const utf8Array = stringToUTF8Bytes("你好");
$log(utf8Array);
}
```

## 新闻.js

```javascript
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

## 有道翻译.js

```javascript
// by leepyer
// 叙白修改适配仓输入法
async function output() {
  try {
    var text = $searchText || $pasteboardContent;
    if (!text) {
      return "请输入要翻译的文本";
    }
    const url = "https://m.youdao.com/translate";
    const params = {
      "inputtext": text,
      "type": "auto"
    };
    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Referer": "https://m.youdao.com/translate"
    };
    const resp = await $http({
      url,
      method: "POST",
      body: params,
      header: headers
    });
    const regex = /<ul id="translateResult">[\s\S]*?<\/ul>/;
    let match = resp.data.match(regex);
    let result = match ? match[0] : null;
    const reg = /(?<=<li>).*(?=<\/li>)/;
    // const reg = /<li>(.*?)<\/li>/;
    const m = result.match(reg);
    const res = m ? m[0] : null;
    // const res = m ? m[1] : null;
    return res;
  } catch (error) {
    $log(error);
    return null;
  }
}
```

## 每日油价.js

```javascript
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

## 汇率.js

```javascript
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

## 热搜.js

```javascript
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

## 谷歌中英互译.js

```javascript
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

## 谷歌翻译.js

```javascript
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

## 进制转换.js

```javascript
// name: 进制转换.js
// date: 2024-09-29
// 输入举例: 二进制格式: 0bxxx, 8进制格式: 0oxxx, 10进制格式: xxx, 16进制格式: 0xXXX
// 结果顺序: 2 8 10 16进制

async function output() {
	const inputStr = $searchText;
  const result = convert(inputStr);
  return result;
}

function convert(inputStr) {
    const results = [];

    // 判断数字的进制
    const base = detectBase(inputStr);

    // 将数字转换为2, 4, 8, 10, 16进制并存入数组
    if (base !== null) {
        const num = parseInt(inputStr, base);
        results.push(num.toString(2));  // 转换成2进制
        results.push(num.toString(8));  // 转换成8进制
        results.push(num.toString(10)); // 转换成10进制
        results.push(num.toString(16).toUpperCase()); // 转换成16进制
    } else {
        return "无法判断输入的进制或输入不合法。";
    }

    return results;
}

// 判断输入数字的进制
function detectBase(str) {
    if (typeof str !== 'string') {
        throw new Error("输入必须是字符串类型。");
    }
    // 使用数组存储正则和对应的进制
    const basePatterns = [
        { pattern: /^0b[01]+$/i, base: 2 },
        { pattern: /^0o[0-7]+$/i, base: 8 },
        { pattern: /^0x[0-9a-f]+$/i, base: 16 },
        { pattern: /^[0-9]+$/, base: 10 }
    ];

    for (const { pattern, base } of basePatterns) {
        if (pattern.test(str)) {
            return base;
        }
    }
    return null;
}
```

## 骂人.js

```javascript
// name: 骂人.js

async function getInsultText(text) {
  try {
    const url = "https://yyapi.a1aa.cn/api.php?level=max";
    

    const resp = await $http({
			url,
      method: 'GET',
      header: { "Content-Type": "application/json" }
    });
    
    // 检查响应是否成功
    if (resp.response.statusCode !== 200) {
      throw new Error(`HTTP error! status: ${resp.response.statusCode}`);
    }

    return resp.data;
  } catch (error) {
    console.error("Translation error:", error);
    return null; // 处理错误的返回值
  }
}

// 示例调用
async function output() {
 
  const result = await getInsultText();
  return result;
};
```

