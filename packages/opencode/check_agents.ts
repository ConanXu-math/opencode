import { Agent } from "./src/agent/agent"

async function main() {
  const agents = await Agent.list()
  console.log("Available agents:")
  agents.forEach((agent) => {
    console.log(`- ${agent.name}: ${agent.description || "No description"} (mode: ${agent.mode})`)
  })
}

main().catch(console.error)
