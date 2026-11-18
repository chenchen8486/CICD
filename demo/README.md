# CI/CD 实操：命令行加法器

　　这个程序接收两个数字并输出它们的和。功能很简单，重点是走完真实仓库中的开发、检查、合并和发布流程。

## 1. 文件各有什么用

- `app/main.py`：加法函数和命令行入口。
- `tests/test_app.py`：三条自动化测试，检查正数、负数和浮点数。
- `../.github/workflows/ci-cd.yml`：GitHub Actions 工作流，负责测试、构建和发布。

## 2. 在本地运行

　　以下命令都从仓库根目录执行。`python` 使用本机已安装的 Python，不需要安装第三方包。

```bash
python demo/app/main.py 2 3
```

　　预期输出：

```text
5
```

　　运行测试：

```bash
cd demo
python -m unittest discover -s tests -v
cd ..
```

　　看到 `Ran 3 tests` 和 `OK` 表示测试通过。构建一个可单独分发的 `.pyz` 文件：

```bash
python -m zipapp demo/app -m "main:main" -o calculator.pyz
python calculator.pyz 10 20
```

　　第二条命令应输出 `30`。`calculator.pyz` 已被 `.gitignore` 排除，构建结果不会提交进源码仓库。

## 3. 第一次拉取请求

1. 打开 [功能分支比较页](https://github.com/chenchen8486/CICD/compare/main...feature/cicd-demo?expand=1)。
2. 确认 base 是 `main`，compare 是 `feature/cicd-demo`，点击 Create pull request。
3. 标题保留为添加 CI/CD 演示项目，点击 Create pull request。
4. 在 PR 页面找到 Checks，等待测试并构建通过。点击 Details 可以查看每条命令的日志。
5. 打开本次运行的 Summary，在 Artifacts 区域下载 `calculator`。
6. 解压后运行 `python calculator.pyz 2 3`，应输出 `5`。

　　这里的 Artifact 是某次构建产生的临时附件，适合检查和传递文件，不等于正式版本。

## 4. 让检查真正拦住合并

1. 进入仓库 Settings，再进入 Branches。
2. 添加适用于 `main` 的分支规则或 ruleset。
3. 启用 Require a pull request before merging。
4. 启用 Require status checks to pass，搜索并选择测试并构建。
5. 保存规则。

　　设置完成后，只有 PR 检查通过才允许合并。不要用管理员权限绕过失败检查，否则看不到 CI 的保护作用。

## 5. 合并并同步本地

　　确认检查为绿色后，在 PR 页面点击 Merge pull request，再点击 Confirm merge。随后在本地执行：

```bash
git switch main
git pull origin main
```

　　`main` 收到合并提交后会再次运行工作流。这次仍不会创建 Release，因为没有推送版本标签。

## 6. 发布第一个版本

　　确认本地 `main` 已包含演示项目，然后执行：

```bash
git tag -a v0.1.0 -m "第一个可运行版本"
git push origin v0.1.0
```

　　标签推送会触发同一套测试和构建。成功后，发布 Release 任务才会运行。打开 [Releases](https://github.com/chenchen8486/CICD/releases)，在 `v0.1.0` 的 Assets 中下载 `calculator.pyz`，运行：

```bash
python calculator.pyz 10 20
```

　　输出 `30` 就说明代码从提交、检查、合并一路走到了可下载的正式版本。

## 7. 观察 CI 如何拦截错误

　　熟悉正常流程后，可以新建分支，把 `return left + right` 临时改成 `return left - right`，提交并创建 PR。三条测试会失败，PR 检查会变红。恢复加法后再次推送，检查会重新运行并恢复绿色。确认理解后可以关闭这个练习 PR，不合并错误代码。
