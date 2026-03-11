import path from "path"
import { mkdir, readdir, readFile, writeFile } from "fs/promises"
import { existsSync } from "fs"

export interface ConversationSummary {
  id: string
  timestamp: string
  sessionId: string
  tags: string[]
  summary: string
  keyPoints: string[]
  codeSnippets: string[]
  originalDialogue: string[]
}

export interface LastNode {
  sessionId: string
  lastMessageId?: string
  lastTimestamp: string
  summaryCount: number
}

export class ConversationSummaryManager {
  private readonly summaryDir: string
  private readonly sessionsDir: string
  private readonly lastNodeFile: string

  constructor() {
    const home = process.env.HOME || process.env.USERPROFILE || "~"
    this.summaryDir = path.join(home, ".opencode", "conversation-summaries", "summaries")
    this.sessionsDir = path.join(home, ".opencode", "conversation-summaries", "sessions")
    this.lastNodeFile = path.join(home, ".opencode", "conversation-summaries", "last-node.json")

    this.ensureDirectories()
  }

  private async ensureDirectories(): Promise<void> {
    const dirs = [this.summaryDir, this.sessionsDir]
    for (const dir of dirs) {
      if (!existsSync(dir)) {
        await mkdir(dir, { recursive: true })
      }
    }
  }

  private getCurrentTimestamp(): string {
    const now = new Date()
    return now.toISOString().replace(/[:.]/g, "-").slice(0, 19)
  }

  private formatDate(timestamp: string): string {
    return timestamp.replace("T", " ").replace(/-/g, "-")
  }

  private async readLastNode(sessionId: string): Promise<LastNode | null> {
    if (!existsSync(this.lastNodeFile)) {
      return null
    }

    try {
      const content = await readFile(this.lastNodeFile, "utf8")
      const data = JSON.parse(content)

      if (data.sessionId === sessionId) {
        return data
      }
      return null
    } catch {
      return null
    }
  }

  private async writeLastNode(node: LastNode): Promise<void> {
    const content = JSON.stringify(node, null, 2)
    await writeFile(this.lastNodeFile, content)
  }

  private generateTags(content: string): string[] {
    const tags: string[] = []
    const text = content.toLowerCase()

    if (text.includes("subagent") || text.includes("agent")) {
      tags.push("#OpenCode配置")
    }
    if (text.includes("代码") || text.includes("编程") || text.includes("开发")) {
      tags.push("#编程")
    }
    if (text.includes("配置") || text.includes("设置") || text.includes("安装")) {
      tags.push("#配置")
    }
    if (text.includes("错误") || text.includes("调试") || text.includes("问题")) {
      tags.push("#调试")
    }
    if (text.includes("学习") || text.includes("教程") || text.includes("解释")) {
      tags.push("#学习")
    }
    if (text.includes("数据库") || text.includes("sql") || text.includes("迁移")) {
      tags.push("#数据库")
    }
    if (text.includes("测试") || text.includes("单元测试") || text.includes("测试用例")) {
      tags.push("#测试")
    }
    if (text.includes("文档") || text.includes("注释") || text.includes("说明")) {
      tags.push("#文档")
    }

    if (tags.length === 0) {
      tags.push("#对话总结")
    }

    return tags
  }

  private extractCodeSnippets(content: string): string[] {
    const codeBlocks: string[] = []
    const lines = content.split("\n")
    let inCodeBlock = false
    let currentBlock: string[] = []

    for (const line of lines) {
      if (line.trim().startsWith("```")) {
        if (inCodeBlock && currentBlock.length > 0) {
          codeBlocks.push(currentBlock.join("\n"))
          currentBlock = []
        }
        inCodeBlock = !inCodeBlock
        continue
      }

      if (inCodeBlock) {
        currentBlock.push(line)
      }
    }

    if (currentBlock.length > 0) {
      codeBlocks.push(currentBlock.join("\n"))
    }

    return codeBlocks
  }

  private extractKeyPoints(content: string): string[] {
    const points: string[] = []
    const lines = content.split("\n")

    for (const line of lines) {
      const trimmed = line.trim()

      if (trimmed.match(/^\d+\.\s/) || trimmed.match(/^[-*]\s/)) {
        points.push(trimmed)
      } else if (trimmed.includes("：") || trimmed.includes(":")) {
        const parts = trimmed.split(/[：:]/)
        if (parts.length >= 2 && parts[0].length < 50) {
          points.push(trimmed)
        }
      }
    }

    if (points.length === 0) {
      const sentences = content.split(/[。.!?]/)
      for (const sentence of sentences) {
        const trimmed = sentence.trim()
        if (trimmed.length > 20 && trimmed.length < 100) {
          points.push(trimmed)
          if (points.length >= 3) break
        }
      }
    }

    return points.slice(0, 5)
  }

  private generateSummary(content: string): string {
    const sentences = content.split(/[。.!?]/)
    const importantSentences = sentences.filter((s) => {
      const trimmed = s.trim()
      return (
        trimmed.length > 10 &&
        (trimmed.includes("需要") ||
          trimmed.includes("应该") ||
          trimmed.includes("可以") ||
          trimmed.includes("建议") ||
          trimmed.includes("问题") ||
          trimmed.includes("解决") ||
          trimmed.includes("实现") ||
          trimmed.includes("功能") ||
          trimmed.includes("配置") ||
          trimmed.includes("设置"))
      )
    })

    if (importantSentences.length > 0) {
      const summary = importantSentences.slice(0, 3).join("。") + "。"
      return summary.length > 300 ? summary.slice(0, 300) + "..." : summary
    }

    if (sentences.length > 0) {
      const firstSentence = sentences[0].trim()
      return firstSentence.slice(0, 200) + (firstSentence.length > 200 ? "..." : "")
    }

    return content.slice(0, 150) + (content.length > 150 ? "..." : "")
  }

  public createSummary(
    sessionId: string,
    dialogue: string[],
    userMessages: string[],
    aiMessages: string[],
  ): ConversationSummary {
    const timestamp = this.getCurrentTimestamp()
    const allContent = dialogue.join("\n")

    const tags = this.generateTags(allContent)
    const summary = this.generateSummary(allContent)
    const keyPoints = this.extractKeyPoints(allContent)
    const codeSnippets = this.extractCodeSnippets(allContent)

    return {
      id: `${timestamp}_${sessionId.slice(0, 8)}`,
      timestamp,
      sessionId,
      tags,
      summary,
      keyPoints,
      codeSnippets,
      originalDialogue: dialogue,
    }
  }

  public async saveSummary(summary: ConversationSummary): Promise<string> {
    const filename = `${summary.timestamp}_session-${summary.sessionId.slice(0, 8)}.md`
    const filepath = path.join(this.summaryDir, filename)

    const content = this.formatSummaryToMarkdown(summary)
    await writeFile(filepath, content)

    const lastNodeData = await this.readLastNode(summary.sessionId)
    const lastNode: LastNode = {
      sessionId: summary.sessionId,
      lastTimestamp: summary.timestamp,
      summaryCount: (lastNodeData?.summaryCount || 0) + 1,
    }
    await this.writeLastNode(lastNode)

    return filepath
  }

  private formatSummaryToMarkdown(summary: ConversationSummary): string {
    const formattedDate = this.formatDate(summary.timestamp)

    let markdown = `# 对话总结 - ${formattedDate}\n\n`
    markdown += `**会话ID**: ${summary.sessionId}\n`
    markdown += `**标签**: ${summary.tags.join(" ")}\n\n`

    markdown += `## 对话摘要\n${summary.summary}\n\n`

    if (summary.keyPoints.length > 0) {
      markdown += `## 关键要点\n`
      for (const point of summary.keyPoints) {
        markdown += `- ${point}\n`
      }
      markdown += `\n`
    }

    if (summary.codeSnippets.length > 0) {
      markdown += `## 相关代码\n`
      for (const snippet of summary.codeSnippets) {
        markdown += `\`\`\`\n${snippet}\n\`\`\`\n\n`
      }
    }

    markdown += `## 原始对话参考\n`
    for (let i = 0; i < summary.originalDialogue.length; i++) {
      const line = summary.originalDialogue[i]
      const prefix = i % 2 === 0 ? "用户" : "AI"
      markdown += `- ${prefix}: "${line.slice(0, 100)}${line.length > 100 ? "..." : ""}"\n`
    }

    return markdown
  }

  public async getSummaryHistory(sessionId?: string): Promise<ConversationSummary[]> {
    const summaries: ConversationSummary[] = []

    if (!existsSync(this.summaryDir)) {
      return summaries
    }

    const files = await readdir(this.summaryDir)
    for (const file of files) {
      if (file.endsWith(".md")) {
        try {
          const content = await readFile(path.join(this.summaryDir, file), "utf8")
          const lines = content.split("\n")

          if (lines.length > 0) {
            const sessionMatch = lines.find((l: string) => l.includes("会话ID"))
            const sessionIdFromFile = sessionMatch ? sessionMatch.split(":")[1]?.trim() : ""

            if (!sessionId || sessionIdFromFile.includes(sessionId.slice(0, 8))) {
              const timestamp = file.split("_session-")[0]
              const tagsMatch = lines.find((l: string) => l.includes("标签"))
              const tags = tagsMatch ? tagsMatch.split(":")[1]?.trim().split(" ") || [] : []

              const summaryStart = lines.findIndex((l: string) => l.includes("## 对话摘要"))
              const summary = summaryStart >= 0 ? lines[summaryStart + 1]?.trim() || "" : ""

              summaries.push({
                id: file.replace(".md", ""),
                timestamp,
                sessionId: sessionIdFromFile,
                tags,
                summary,
                keyPoints: [],
                codeSnippets: [],
                originalDialogue: [],
              })
            }
          }
        } catch {
          continue
        }
      }
    }

    return summaries.sort((a, b) => b.timestamp.localeCompare(a.timestamp))
  }
}
