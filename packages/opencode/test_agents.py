#!/usr/bin/env python3
"""
测试 agent 配置是否被正确加载
"""

import os
import sys
import yaml
import json
from pathlib import Path


def test_markdown_agents():
    """测试 Markdown 格式的 agent 文件"""
    agents_dir = Path(".opencode/agents")
    print(f"检查目录: {agents_dir.absolute()}")

    if not agents_dir.exists():
        print("❌ agents 目录不存在")
        return []

    agents = []
    for md_file in agents_dir.glob("*.md"):
        print(f"\n📄 找到文件: {md_file.name}")

        try:
            content = md_file.read_text()
            # 解析 frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    data = yaml.safe_load(frontmatter)

                    agent_name = md_file.stem
                    description = data.get("description", "No description")
                    mode = data.get("mode", "subagent")

                    print(f"  名称: {agent_name}")
                    print(f"  描述: {description[:50]}...")
                    print(f"  模式: {mode}")

                    agents.append(agent_name)
        except Exception as e:
            print(f"  解析错误: {e}")

    return agents


def test_json_config():
    """测试 JSON 配置中的 agent"""
    config_file = Path("opencode.json")
    print(f"\n检查配置文件: {config_file.absolute()}")

    if not config_file.exists():
        print("❌ opencode.json 不存在")
        return []

    try:
        with open(config_file, "r") as f:
            config = json.load(f)

        agents = config.get("agent", {})
        print(f"找到 {len(agents)} 个 JSON 配置的 agent:")

        for name, agent_config in agents.items():
            description = agent_config.get("description", "No description")
            mode = agent_config.get("mode", "subagent")
            print(f"  {name}: {description[:50]}... ({mode})")

        return list(agents.keys())
    except Exception as e:
        print(f"❌ 解析 JSON 错误: {e}")
        return []


def main():
    print("🔍 测试 agent 配置加载...")
    print("=" * 50)

    md_agents = test_markdown_agents()
    json_agents = test_json_config()

    print("\n" + "=" * 50)
    print("📋 汇总结果:")
    print(f"Markdown agents: {', '.join(md_agents) if md_agents else '无'}")
    print(f"JSON agents: {', '.join(json_agents) if json_agents else '无'}")

    all_agents = set(md_agents + json_agents)
    print(f"\n✅ 总共 {len(all_agents)} 个 agent: {', '.join(all_agents)}")

    # 检查 open-evolve 是否存在
    if "open-evolve" in all_agents:
        print("\n🎯 open-evolve 已正确配置！")
        print("尝试在 opencode 中输入: @open-evolve 你好")
    else:
        print("\n❌ open-evolve 未找到，请检查配置")


if __name__ == "__main__":
    main()
