import { ConversationSummaryManager } from "./conversation-summary"

async function test() {
  const manager = new ConversationSummaryManager()

  const sessionId = "test-session-123"
  const dialogue = [
    "用户：我想内置一个subagent，每次把我的对话总结整理为md，保存在本地文件夹里",
    "AI：明白。你想要一个subagent，功能是：1. 每次调用时，将从上一次调用到本次调用之间的对话内容总结为markdown 2. 保存到本地文件夹 3. 创建新的时间节点，等待下一次调用",
    "用户：就是你要从对话中提取一些可总结的经验或者我提问的重点，可以是文摘要，但是需要带一个标签",
    "AI：需要确认几个细节：1. 总结格式：纯文本摘要还是结构化记录？2. 保存位置：固定文件夹还是可配置？3. 节点标识：用时间戳、序号还是其他方式？4. 是否要保留原始对话内容？",
  ]

  const userMessages = [
    "用户：我想内置一个subagent，每次把我的对话总结整理为md，保存在本地文件夹里",
    "用户：就是你要从对话中提取一些可总结的经验或者我提问的重点，可以是文摘要，但是需要带一个标签",
  ]

  const aiMessages = [
    "AI：明白。你想要一个subagent，功能是：1. 每次调用时，将从上一次调用到本次调用之间的对话内容总结为markdown 2. 保存到本地文件夹 3. 创建新的时间节点，等待下一次调用",
    "AI：需要确认几个细节：1. 总结格式：纯文本摘要还是结构化记录？2. 保存位置：固定文件夹还是可配置？3. 节点标识：用时间戳、序号还是其他方式？4. 是否要保留原始对话内容？",
  ]

  const summary = manager.createSummary(sessionId, dialogue, userMessages, aiMessages)
  console.log("生成的总结:", JSON.stringify(summary, null, 2))

  const filepath = await manager.saveSummary(summary)
  console.log("保存到:", filepath)

  const history = await manager.getSummaryHistory(sessionId)
  console.log("历史记录:", history.length, "条")
}

test().catch(console.error)
