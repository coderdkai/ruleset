# RuleSet

> 个人专属代理分流规则集与自动化管理工具包，设计为与上游社区规则（如 ACL4SSR）解耦并优先覆盖。

## 🌟 核心理念与分层设计

1. **绝对优先覆盖**：个人专属规则排在配置文件最前列（第一优先级），遇到任何冲突以个人规则为最高准则。
2. **免冲突追新**：第二优先级直接挂接上游官方开源规则集（如 ACL4SSR），无需反复 Git Rebase/Merge 解决冲突，上游日常维护的冷门域名静默自动同步。
3. **CLI 快速运维**：内置 `scripts/add_rule.py`，一行命令快速追加新域名、查重、排序并自动 `git push`。

---

## 📂 规则订阅链接（Raw / CDN）

| 规则集名称 | 说明 | GitHub Raw 链接 |
| :--- | :--- | :--- |
| **`AI.list`** | 全面 AI 规则（含 Cursor、xAI、Windsurf、v0、Lovable 等） | `https://raw.githubusercontent.com/coderdkai/ruleset/master/Clash/Ruleset/AI.list` |
| **`LinuxDo.list`** | Linux.do 论坛与配套服务体系 | `https://raw.githubusercontent.com/coderdkai/ruleset/master/Clash/Ruleset/LinuxDo.list` |
| **`ProxyGFW.list`** | 个人最高优先级强制代理域名 | `https://raw.githubusercontent.com/coderdkai/ruleset/master/Clash/Ruleset/ProxyGFW.list` |
| **`UnBan.list`** | 个人最高优先级强制直连域名 | `https://raw.githubusercontent.com/coderdkai/ruleset/master/Clash/Ruleset/UnBan.list` |

---

## 🛠️ CLI 快速追加规则

在本地通过 Python 脚本可以瞬间完成域名追加、校验与推送：

```bash
# 1. 默认向 AI 规则追加域名
python3 scripts/add_rule.py -d cursorapi.com

# 2. 追加公司内网直连域名并直接推送远端
python3 scripts/add_rule.py -r UnBan -t DOMAIN -d intranet.mycorp.com --push

# 3. 追加强制代理域名并附带备注
python3 scripts/add_rule.py -r ProxyGFW -d api.someworkspace.org -c "个人VPS服务" --push

# 4. 批量去重与格式化全部规则
python3 scripts/format_rule.py
```

---

## 🧩 Sub-Store 与 Clash / Mihomo 快速装配

完整示例模板请参考 [templates/sub-store-artifact.yaml](templates/sub-store-artifact.yaml)。

核心规则排列顺序：
```yaml
rules:
  # 1. 第一优先级：个人专属规则
  - RULE-SET,my-unban,🎯 全球直连
  - RULE-SET,my-proxy,🚀 默认代理
  - RULE-SET,my-linuxdo,🐧 LinuxDo
  - RULE-SET,my-ai,🤖 AI服务

  # 2. 第二优先级：上游官方规则
  - RULE-SET,upstream-ai,🤖 AI服务
  - RULE-SET,upstream-telegram,🚀 默认代理

  # 3. 兜底
  - GEOSITE,cn,🎯 全球直连
  - GEOIP,cn,🎯 全球直连
  - MATCH,🚀 默认代理
```
