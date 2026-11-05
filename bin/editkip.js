#!/usr/bin/env node
"use strict";
const fs = require("fs");
const path = require("path");
const os = require("os");

const ROOT = path.join(__dirname, "..");
const HOME = os.homedir();
const pkg = require(path.join(ROOT, "package.json"));
const args = process.argv.slice(2);

const has = (f) => args.includes(f);
const val = (f) => {
  const i = args.indexOf(f);
  return i > -1 && args[i + 1] && !args[i + 1].startsWith("-") ? args[i + 1] : null;
};

if (has("--help") || has("-h")) {
  console.log(`Editkip ${pkg.version}: AI video-editing skill for CapCut

Usage: npx editkip [options]

  (no options)           install globally into every detected agent
  --agent <name>         antigravity | claude | all   (default: detected)
  --workspace [dir]      install into a workspace instead of globally (default: cwd)
  --uninstall            remove Editkip
  --version, --help
`);
  process.exit(0);
}
if (has("--version") || has("-v")) {
  console.log(pkg.version);
  process.exit(0);
}

const wsFlag = has("--workspace");
const wsDir = wsFlag ? path.resolve(val("--workspace") || process.cwd()) : null;

const AGENTS = {
  antigravity: {
    label: "Antigravity",
    detect: () => fs.existsSync(path.join(HOME, ".gemini")),
    skills: () => wsDir ? path.join(wsDir, ".agent", "skills") : path.join(HOME, ".gemini", "antigravity", "skills"),
    commands: () => wsDir ? path.join(wsDir, ".agent", "workflows") : path.join(HOME, ".gemini", "antigravity", "global_workflows"),
  },
  claude: {
    label: "Claude Code",
    detect: () => fs.existsSync(path.join(HOME, ".claude")),
    skills: () => wsDir ? path.join(wsDir, ".claude", "skills") : path.join(HOME, ".claude", "skills"),
    commands: () => wsDir ? path.join(wsDir, ".claude", "commands") : path.join(HOME, ".claude", "commands"),
  },
};

let chosen;
const agentArg = val("--agent");
if (agentArg && agentArg !== "all") {
  if (!AGENTS[agentArg]) {
    console.error(`Unknown agent "${agentArg}". Use: ${Object.keys(AGENTS).join(", ")}, all`);
    process.exit(1);
  }
  chosen = [agentArg];
} else if (agentArg === "all" || wsFlag) {
  chosen = Object.keys(AGENTS);
} else {
  chosen = Object.keys(AGENTS).filter((k) => AGENTS[k].detect());
}

if (!chosen.length) {
  console.error("No supported agent found (looked for ~/.gemini and ~/.claude).\nRun again with --agent antigravity | claude | all.");
  process.exit(1);
}

const cmdFiles = fs.readdirSync(path.join(ROOT, "workflows")).filter((f) => f.endsWith(".md"));
const scope = wsDir ? `workspace ${wsDir}` : "global";

for (const key of chosen) {
  const a = AGENTS[key];
  const skillDest = path.join(a.skills(), "editkip");
  const cmdDir = a.commands();
  try {
    if (has("--uninstall")) {
      fs.rmSync(skillDest, { recursive: true, force: true });
      for (const f of cmdFiles) fs.rmSync(path.join(cmdDir, f), { force: true });
      console.log(`- ${a.label}: removed (${scope})`);
    } else {
      fs.rmSync(skillDest, { recursive: true, force: true });
      fs.mkdirSync(a.skills(), { recursive: true });
      fs.cpSync(path.join(ROOT, "skills", "editkip"), skillDest, { recursive: true });
      fs.mkdirSync(cmdDir, { recursive: true });
      for (const f of cmdFiles) fs.copyFileSync(path.join(ROOT, "workflows", f), path.join(cmdDir, f));
      console.log(`+ ${a.label} (${scope})\n    skill:    ${skillDest}\n    commands: ${cmdDir}`);
    }
  } catch (e) {
    console.error(`! ${a.label}: ${e.message}`);
    process.exitCode = 1;
  }
}

if (!has("--uninstall") && !process.exitCode) {
  console.log("\nDone. Open a workspace folder in your agent and run /editkip-setup");
  console.log("Needs: CapCut desktop (closed while editing), Python 3.9+, ffmpeg.");
}
