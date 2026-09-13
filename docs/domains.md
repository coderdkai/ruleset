# 服务域名与基础设施字典 (Domains Reference)

> 本文档用于归档收录各大 AI 厂商及合规金融/交易所的官方域名、专有子域、后台关键基础设施端点，方便随时翻阅、快速拿取并同步至规则集。

---

## 🎯 规则设计准则 (Design Principles)

1. **厂商自有资产全面统一为 `DOMAIN-SUFFIX`**：
   - 彻底废除零散重复的完整 `DOMAIN`，直接使用根域名或厂商二级域名的 `DOMAIN-SUFFIX` 覆盖全部子端点与静态 CDN。
   - 例如：`anthropic.com`、`claude.ai`、`grok.com`、`binance.com`、`okx.com`。
2. **专属多租户风控端点**：
   - 采用**带厂商前缀的针对性 `DOMAIN-SUFFIX`**（如 `DOMAIN-SUFFIX,openai-api.arkoselabs.com`），既满足后缀匹配规范，又死死锁定该租户，100% 杜绝误伤其他网站。
3. **安全验证盾（如 Cloudflare Turnstile）**：
   - `challenges.cloudflare.com` **严禁**单独分流到异地节点，否则会触发 Cloudflare 跨 IP 验签失败导致验证卡死（死循环）。必须随主请求保持同路。
4. **支付与金融中间件隔离原则**：
   - 通用支付（Stripe、PayPal）、银行 3DS 验证域名**严禁进入 AI 规则集**，仅在此文档中做技术排查归档。

---

## 1. OpenAI / ChatGPT / Sora

### 独占顶级/二级域名 (`DOMAIN-SUFFIX`)
- `openai.com`
- `chatgpt.com`
- `ai.com`
- `sora.com`
- `o3.com`
- `oaistatic.com`
- `oaiusercontent.com`
- `openaicom.imgix.net`
- `chatgpt.livekit.cloud`
- `host.livekit.cloud`
- `turn.livekit.cloud`

### 专属风控与防降智端点 (`DOMAIN-SUFFIX`)
- `openai-api.arkoselabs.com` (ArkoseLabs 专用真人验证)
- `client-api.arkoselabs.com`
- `api.statsig.com` (Statsig 灰度门控，防降智核心)
- `events.statsigapi.net`
- `featuregates.org`

### 微软 Azure 后端路由与 Blob 存储 (`DOMAIN-SUFFIX`)
- `openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net`
- `openaicomproductionae4b.blob.core.windows.net`
- `production-openaicom-storage.azureedge.net`
- `openaiapi-site.azureedge.net`
- `chat.openai.com.cdn.cloudflare.net`
- `openai.com.cdn.cloudflare.net`

---

## 2. Anthropic / Claude

### 独占顶级/二级域名 (`DOMAIN-SUFFIX`)
- `anthropic.com`
- `claude.ai`
- `claude.site`
- `claudeforwork.com`
- `cdn.usefathom.com`

---

## 3. Google Gemini / AI Studio / DeepMind

### 独占顶级/二级域名 (`DOMAIN-SUFFIX`)
- `gemini.google.com`
- `bard.google.com`
- `aistudio.google.com`
- `makersuite.google.com`
- `deepmind.com`
- `deepmind.google`
- `generativeai.google`
- `ai.google.dev`
- `generativelanguage.googleapis.com`
- `alkalimakersuite-pa.clients6.google.com`
- `proactivebackend-pa.googleapis.com`

---

## 4. xAI / Grok

### 独占域名与业务端点 (`DOMAIN-SUFFIX`)
- `x.ai`
- `grok.com`

---

## 5. Microsoft Copilot

### 核心域名与分流端点 (`DOMAIN-SUFFIX`)
- `copilot.microsoft.com`
- `sydney.bing.com` (Sydney 核心对话代号)
- `edgeservices.bing.com` (Edge 侧边栏 Copilot 接口)
- `gateway.bingviz.microsoft.net` (Copilot 网关)
- `gateway.bingviz.microsoftapp.net` (Copilot App 网关)

---

## 6. AI 编程工具与生态 (IDE & Extensions)

- **Cursor**: `cursor.com`, `cursor.sh`, `cursor-cdn.com`, `cursorapi.com`, `todesktop.com`, `todesktop-cdn.com`
- **Windsurf / Codeium**: `windsurf.ai`, `codeium.com`, `codeiumdata.com`
- **GitHub Copilot**: `githubcopilot.com`, `copilot.github.com`, `api.githubcopilot.com`, `copilot-proxy.githubusercontent.com`, `copilot-telemetry.githubusercontent.com`
- **Augment Code**: `augmentcode.com`

---

## 7. 新一代 AI 构建与生成应用

- **v0**: `v0.dev`
- **Lovable**: `lovable.dev`
- **Bolt**: `bolt.new`

---

## 8. 推理 API、聚合平台与多媒体

- **推理/模型**: `groq.com`, `cerebras.ai`, `together.ai`, `together.xyz`, `cohere.com`, `cohere.ai`, `mistral.ai`, `perplexity.ai`, `pplx.ai`, `poe.com`, `replicate.com`
- **多媒体生成**: `midjourney.com`, `suno.ai`, `suno.com`, `elevenlabs.io`, `fal.ai`, `fal.run`
- **生态与镜像**: `oaifree.com`, `sharedchat.cn`

---

## 9. 主流加密货币交易所 (Crypto Exchanges)

> ⚠️ **风控与地区限制注意事项**：
> - **受限地区**：Binance / OKX 对美国（US）、日本（JP）、新加坡（SG）、加拿大（CA）以及英国（UK）等地的 IP 有强监管限制，访问时会强制跳转或弹窗拒绝服务。
> - **建议落地**：建议在策略组 `🪙 加密货币` 中指定**台湾（TW）**、部分欧洲非受限地区节点或稳定直连。

### 币安 (Binance)
- 核心业务：`binance.com`, `binance.net`, `binance.org`, `binance.cloud`, `binance.charity`, `binance.vision`
- 国内/全球备用：`binancezh.com`, `binancezh.net`, `binancezh.info`, `binancezh.pro`, `binancezh.top`, `binancezh.biz`, `binancezh.mobi`
- 静态 CDN 与生态：`bnbstatic.com`, `bntrace.com`, `saasexch.com`, `trustwallet.com`

### 欧易 (OKX)
- 核心主站：`okx.com`, `okx.net`, `okex.com`
- 专用 CDN 与 DNS：`oklink.com`, `okcdn.com`, `okx-static.com`, `okx-dns.com`, `okx-dns1.com`, `okx-dns2.com`

### Bybit
- `bybit.com`, `bybit-global.com`, `bycsi.com`

---

## ⚠️ 附录：支付与风控中间件（仅归档备查，坚决不入分流规则）

当排查 ChatGPT Plus / Claude Pro 订阅绑卡失败时，以下域名仅用于网络日志核验：
- **Stripe 核心资产**：`stripe.com`, `js.stripe.com`, `api.stripe.com`, `m.stripe.com`, `link.com`
- **支付身份验证**：`auth0.com`
- **发卡行 3DS 验证**：各银行自建验证网关（随发卡行动态变化，必须走通用代理或直连，不可强制指定 AI 专线）。
