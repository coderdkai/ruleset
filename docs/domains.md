# AI 服务域名与基础设施字典 (Domains Reference)

> 本文档用于归档收录各大 AI 厂商的官方域名、专有子域、后台关键基础设施端点，方便随时翻阅、快速拿取并同步至规则集。

---

## 🎯 规则设计准则 (Design Principles)

1. **厂商自有独占资产**：优先且必须使用 `DOMAIN-SUFFIX`。
   - 例如：`openai.com`、`claude.ai`、`grok.com`、`cursor.com`。
   - 效果：一条规则直接覆盖主站、API、各地区集群及静态 CDN，无副作用且免维护。
2. **多租户公有云 / 通用 SaaS 基础设施**：必须严格使用完整 `DOMAIN` 精准匹配。
   - 例如：`openai-api.arkoselabs.com`（Arkose 验证码）、`api.statsig.com`（Statsig 灰度门控）、`production-openaicom-storage.azureedge.net`。
   - 效果：防止因通用域名后缀导致其他正常网站、国内直连业务被强行拽入 AI 专线。
3. **安全验证盾（如 Cloudflare Turnstile）**：
   - `challenges.cloudflare.com` **严禁**单独分流到异地节点，否则会触发 Cloudflare 跨 IP 验签失败导致验证卡死（死循环）。必须随主请求保持同路。

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

### 关键基础设施与防降智端点 (`DOMAIN` 精准匹配)
- **风控与专用验证码**：
  - `openai-api.arkoselabs.com`
  - `client-api.arkoselabs.com`
- **功能灰度与特征开关 (防降智核心)**：
  - `api.statsig.com`
  - `events.statsigapi.net`
  - `featuregates.org` (`DOMAIN-SUFFIX`)
- **微软 Azure 后端路由与 Blob 存储**：
  - `openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net`
  - `openaicomproductionae4b.blob.core.windows.net`
  - `production-openaicom-storage.azureedge.net`
  - `openaiapi-site.azureedge.net`
  - `chat.openai.com.cdn.cloudflare.net`

---

## 2. Anthropic / Claude

### 独占顶级/二级域名 (`DOMAIN-SUFFIX`)
- `anthropic.com`
- `claude.ai`
- `claude.site`
- `claudeforwork.com`

### 关键接口与统计 (`DOMAIN`)
- `api.anthropic.com`
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
- `proactivebackend-pa.googleapis.com`

### 开发者接口与专属端点 (`DOMAIN` / `DOMAIN-KEYWORD`)
- `ai.google.dev`
- `alkalimakersuite-pa.clients6.google.com`
- `DOMAIN-KEYWORD,generativelanguage` (覆盖 `generativelanguage.googleapis.com` 全区域)

---

## 4. xAI / Grok

### 独占域名与业务端点 (`DOMAIN-SUFFIX` / `DOMAIN`)
- `x.ai`
- `grok.com`
- `api.x.ai`
- `assets.grok.com`
- `code.grok.com`
- `cli-chat-proxy.grok.com`

---

## 5. Microsoft Copilot

### 核心域名与分流端点 (`DOMAIN-SUFFIX` / `DOMAIN`)
- `copilot.microsoft.com`
- `sydney.bing.com` (Sydney 核心对话代号)
- `edgeservices.bing.com` (Edge 侧边栏 Copilot 接口)
- `gateway.bingviz.microsoft.net` (Copilot 网关)
- `gateway.bingviz.microsoftapp.net` (Copilot App 网关)

---

## 6. AI 编程工具与生态 (IDE & Extensions)

- **Cursor**: `cursor.com`, `cursor.sh`, `cursor-cdn.com`, `cursorapi.com`, `todesktop.com`, `todesktop-cdn.com`
- **Windsurf / Codeium**: `windsurf.ai`, `codeium.com`, `codeiumdata.com`
- **GitHub Copilot**: `githubcopilot.com`, `api.githubcopilot.com`, `copilot-proxy.githubusercontent.com`, `copilot-telemetry.githubusercontent.com`
- **Augment Code**: `augmentcode.com`

---

## 7. 新一代 AI 构建与生成应用

- **v0**: `v0.dev`
- **Lovable**: `lovable.dev`
- **Bolt**: `bolt.new`

---

## 8. 推理 API、聚合平台与社区镜像

- **推理/模型**: `groq.com`, `cerebras.ai`, `together.ai`, `together.xyz`, `cohere.com`, `cohere.ai`, `mistral.ai`, `perplexity.ai`, `pplx.ai`, `poe.com`, `replicate.com`
- **多媒体生成**: `midjourney.com`, `suno.ai`, `suno.com`, `elevenlabs.io`, `fal.ai`, `fal.run`
- **社区与镜像**: `linux.do`, `oaifree.com`, `sharedchat.cn`
