# 一键：为 session-evolution-graph 添加 Topics / 描述，并 Pin 到个人主页
# 使用前请先执行一次：gh auth login

$ErrorActionPreference = "Stop"
$Owner = "quick123-666"
$Repo = "session-evolution-graph"

Write-Host "==> 检查 GitHub CLI 登录状态..." -ForegroundColor Cyan
gh auth status 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "未登录。请先运行： gh auth login" -ForegroundColor Yellow
    Write-Host "登录完成后重新执行本脚本。" -ForegroundColor Yellow
    exit 1
}

Write-Host "==> 设置仓库描述与 Topics..." -ForegroundColor Cyan
gh repo edit "$Owner/$Repo" `
    --description "从 AI 会话提炼问题演化图谱 · Agent 教学课（中英双语 README）" `
    --add-topic "agent" `
    --add-topic "llm" `
    --add-topic "knowledge-graph" `
    --add-topic "python" `
    --add-topic "graph" `
    --add-topic "evolution-graph" `
    --add-topic "graphspec" `
    --add-topic "teaching" `
    --add-topic "harness" `
    --add-topic "session-memory"

if ($LASTEXITCODE -ne 0) { throw "repo edit 失败" }
Write-Host "    Topics 与描述已更新。" -ForegroundColor Green

# Pin 顺序（最多 6 个，按展示优先级）
$PinRepos = @(
    "toolchain-manager-course",
    "session-evolution-graph",
    "star-level",
    "bounded-memory",
    "code-memex-lite",
    "Claude-Bridge-claw"
)

Write-Host "==> 获取仓库 Node ID..." -ForegroundColor Cyan
$repoIds = @()
foreach ($name in $PinRepos) {
    $q = "query { repository(owner: `"$Owner`", name: `"$name`") { id name } }"
    $json = gh api graphql -f query=$q 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    跳过不存在的仓库: $name" -ForegroundColor DarkYellow
        continue
    }
    $id = ($json | ConvertFrom-Json).data.repository.id
    if ($id) {
        $repoIds += @{ name = $name; id = $id }
        Write-Host "    OK $name" -ForegroundColor DarkGray
    }
}

if ($repoIds.Count -eq 0) {
    Write-Host "没有可 Pin 的仓库，请检查仓库名。" -ForegroundColor Red
    exit 1
}

Write-Host "==> 获取用户 Node ID..." -ForegroundColor Cyan
$userJson = gh api graphql -f query="query { user(login: `"$Owner`") { id } }"
$userId = ($userJson | ConvertFrom-Json).data.user.id

$pinnedItems = ($repoIds | ForEach-Object {
    "{ repositoryId: `"$($_.id)`", type: REPOSITORY }"
}) -join ", "

$mutation = @"
mutation {
  updatePinnedItems(input: {
    ownerId: "$userId",
    pinnedItems: [ $pinnedItems ]
  }) {
    owner { ... on User { login pinnedItems(first: 6, types: REPOSITORY) {
      nodes { ... on Repository { name } }
    }}}}
  }
}
"@

Write-Host "==> Pin 到个人主页（最多 6 个）..." -ForegroundColor Cyan
$result = gh api graphql -f query=$mutation 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "GraphQL Pin 失败（部分账号可能不支持 API Pin）。" -ForegroundColor Yellow
    Write-Host $result
    Write-Host ""
    Write-Host "请手动 Pin：" -ForegroundColor Yellow
    Write-Host "  1. 打开 https://github.com/$Owner"
    Write-Host "  2. Customize your pins"
    Write-Host "  3. 勾选: $($PinRepos -join ', ')"
    Start-Process "https://github.com/$Owner?pin=1"
    exit 0
}

$pinned = ($result | ConvertFrom-Json).data.updatePinnedItems.owner.pinnedItems.nodes
Write-Host "    已 Pin:" -ForegroundColor Green
$pinned | ForEach-Object { Write-Host "      - $($_.name)" }

Write-Host ""
Write-Host "完成！主页: https://github.com/$Owner" -ForegroundColor Green
Write-Host "仓库:   https://github.com/$Owner/$Repo" -ForegroundColor Green
