# GitHub CI/CD 演示项目 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用一个命令行加法器跑通 GitHub 上的测试、构建、拉取请求和 Release 发布。

**Architecture:** `demo/` 保存程序与测试，根目录工作流先执行测试和构建，再上传 Artifact。标签推送在同一个工作流中触发第二个任务，下载同一产物并创建 GitHub Release。

**Tech Stack:** Python 3.13、标准库 `argparse` / `unittest` / `zipapp`、GitHub Actions、GitHub CLI（仅运行器预装）。

**Spec:** `docs/superpowers/specs/2026-11-18-github-cicd-demo-design.md`

## Global Constraints

- 不安装第三方 Python 依赖。
- 只有 `v*` 标签可以创建 Release。
- 本地与云端使用相同测试命令。
- 不改动现有教程正文。

## Review Focus

- 正数、负数和浮点数相加应得到正确结果，由任务 1 的单元测试覆盖。
- 缺少参数或传入非数字时，命令行应给出错误并返回非零状态，由任务 1 的命令行检查覆盖。
- 非标签提交不能发布，由任务 2 的任务条件约束并在首次 main 构建中确认。
- 标签发布必须使用刚通过测试的产物，由任务 2 的依赖与下载步骤保证。
- 构建产物应能独立运行，由任务 2 的 `.pyz` 实际执行检查覆盖。

---

### Task 1: 最小程序与测试

**Files:**
- Create: `demo/app/main.py`
- Create: `demo/tests/test_app.py`
- Create: `.gitignore`
- Test: `demo/tests/test_app.py`

**Interfaces:**
- Produces: `add(left: float, right: float) -> float` 与 `main() -> None`。
- 命令行： `python app/main.py 2 3` 输出 `5`。

- [ ] **Step 1: 编写失败测试**

测试 `add(2, 3) == 5`、`add(-1, 1) == 0`、`add(0.1, 0.2) == pytest 近似值`，但不得引入 pytest，改用 `assertAlmostEqual(0.3)`。

- [ ] **Step 2: 验证测试先失败**

Run: `cd demo && python -m unittest discover -s tests -v`
Expected: 因 `app.main` 尚不存在而失败。

- [ ] **Step 3: 实现加法函数与命令行入口**

使用 `argparse` 接收两个 `float` 参数，以 `g` 格式打印结果。

- [ ] **Step 4: 验证程序和测试**

Run: `cd demo && python -m unittest discover -s tests -v && python app/main.py 2 3`
Expected: 测试全部通过，程序输出 `5`。

### Task 2: CI 构建与标签发布

**Files:**
- Create: `.github/workflows/ci-cd.yml`
- Create: `demo/README.md`
- Test: `.github/workflows/ci-cd.yml`

**Interfaces:**
- Consumes: 任务 1 的程序、测试和命令。
- Produces: Artifact `calculator`，其中包含 `calculator.pyz`；标签 `v0.1.0` 对应 Release。

- [ ] **Step 1: 编写单工作流**

`test-and-build` 在 main、PR、手动触发和标签上测试并打包；`release` 仅在标签事件运行，依赖前者并使用 `contents: write`。

- [ ] **Step 2: 本地执行云端核心命令**

Run: `python -m zipapp demo/app -m "main:main" -o dist/calculator.pyz && python dist/calculator.pyz 2 3`
Expected: 输出 `5`。

- [ ] **Step 3: 检查并提交**

检查 YAML 结构与 Git diff，提交后推送 main，在 Actions 页面确认测试和构建成功、Artifact 可下载且没有 Release 任务。

- [ ] **Step 4: 用户实操**

在功能分支制造一次可见的小改动，发起 PR 并观察检查，合并后创建 `v0.1.0` 标签，确认 Release 中可下载并运行 `calculator.pyz`。
