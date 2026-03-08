#!/usr/bin/env python3
"""
使用 Playwright 注册 GitHub 账号
"""

import asyncio
from playwright.async_api import async_playwright

async def register_github():
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("🌐 访问 GitHub 注册页面...")
        await page.goto("https://github.com/signup")
        
        # 等待页面加载
        await page.wait_for_timeout(3000)
        
        # 截图看看当前状态
        await page.screenshot(path="/tmp/github_signup.png")
        print("📸 截图保存到 /tmp/github_signup.png")
        
        # 获取页面内容
        content = await page.content()
        print("📄 页面标题:", await page.title())
        
        await browser.close()
        print("✅ 浏览器已关闭")

if __name__ == "__main__":
    asyncio.run(register_github())
