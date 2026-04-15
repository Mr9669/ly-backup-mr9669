# OpenClaw 安全审计报告

**时间：** 2026-04-14 13:05
**审计类型：** 标准安全审计
**审计结果：** 4个Critical + 5个Warn + 1个Info

---

## 🚨 Critical级别问题（必须立即修复）

### 1. Control UI 设备认证被禁用
```
CRITICAL DANGEROUS: Control UI device auth disabled
gateway.controlUi.dangerouslyDisableDeviceAuth=true disables device identity checks for the Control UI.
```
**风险：** 控制UI未进行设备身份验证，任何人都可能访问
**修复：** 除非在紧急情况下，否则禁用此选项

### 2. 开放的 groupPolicy 启用了高级工具
```
CRITICAL Open groupPolicy with elevated tools enabled
Found groupPolicy="open" at: - channels.feishu.groupPolicy
```
**风险：** 在开放群组中启用高级工具，提示注入可能造成严重影响
**修复：** 设置 groupPolicy="allowlist" 并严格控制白名单

### 3. 开放的 groupPolicy 暴露了运行时/文件系统工具
```
CRITICAL Open groupPolicy with runtime/filesystem tools exposed
Found groupPolicy="open" at: - channels.feishu.groupPolicy
Risky tool exposure contexts:
- agents.defaults (sandbox=off; runtime=[exec, process]; fs=[read, write])
```
**风险：** 暴露了危险的运行时和文件系统工具
**修复：** 对于开放群组，使用 tools.profile="messaging"，设置 tools.fs.workspaceOnly=true，使用 agents.defaults.sandbox.mode="all"

### 4. 飞书安全警告
```
CRITICAL Feishu security warning
Feishu[default] groups: groupPolicy="open" allows any group to interact (mention-gated).
```
**风险：** 飞书群组策略设置为"open"，任何群组都可以交互
**修复：** 设置 groupPolicy="allowlist" 并严格控制允许的群组

---

## ⚠️ Warn级别问题（需要尽快修复）

### 1. 飞书文档创建权限
```
WARN Feishu doc create can grant requester permissions
channels.feishu tools include "doc"; feishu_doc action "create" can grant document access to the trusted requesting Feishu user.
```
**风险：** 飞书文档创建功能可以授予请求者文档访问权限
**修复：** 不需要时禁用 channels.feishu.tools.doc，限制不受信任提示的工具访问

### 2. 不安全的配置标志
```
WARN Insecure or dangerous config flags enabled
Detected 1 enabled flag(s): gateway.controlUi.dangerouslyDisableDeviceAuth=true.
```
**风险：** 启用了不安全或危险的配置标志
**修复：** 不在调试时禁用这些标志，或将部署范围限制为受信任/仅本地的网络

### 3-5. 其他警告（需要详细审计查看）

---

## 📊 安全评分

| 级别 | 数量 | 优先级 |
|------|------|--------|
| Critical | 4 | 🔴 P0 - 立即修复 |
| Warn | 5 | 🟡 P1 - 尽快修复 |
| Info | 1 | 🟢 P2 - 计划修复 |

**总体安全等级：** 🚨 高危

---

## 🔧 立即行动建议

### 第一优先级（今日完成）
1. ✅ 启用 Control UI 设备认证
2. ✅ 将飞书 groupPolicy 改为 "allowlist"
3. ✅ 禁用不必要的运行时/文件系统工具
4. ✅ 限制高级工具白名单

### 第二优先级（本周完成）
1. ✅ 配置沙箱模式（sandbox.mode="all"）
2. ✅ 限制文件系统访问（fs.workspaceOnly=true）
3. ✅ 禁用飞书文档创建工具（如不需要）

### 第三优先级（本月完成）
1. ✅ 完整深度安全审计
2. ✅ 定期安全扫描
3. ✅ 建立安全监控机制

---

## 📝 备注

- 当前环境为本地开发环境（127.0.0.1）
- 飞书群组策略为"开放"状态
- 未启用Tailscale VPN
- Gateway运行在本地回环地址

**下一步：** 执行深度安全审计并制定详细修复计划
