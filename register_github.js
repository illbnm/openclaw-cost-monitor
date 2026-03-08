const puppeteer = require('puppeteer');

async function registerGitHub() {
    console.log('🚀 启动浏览器...');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: '/home/node/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    });
    
    const page = await browser.newPage();
    
    console.log('🌐 访问 GitHub 注册页面...');
    await page.goto('https://github.com/signup', { waitUntil: 'networkidle2' });
    
    // 截图
    await page.screenshot({ path: '/tmp/github_signup.png', fullPage: true });
    console.log('📸 截图保存到 /tmp/github_signup.png');
    
    // 获取页面信息
    const title = await page.title();
    console.log('📄 页面标题:', title);
    
    // 获取表单字段
    const inputs = await page.$$eval('input', inputs => 
        inputs.map(i => ({ name: i.name, id: i.id, type: i.type, placeholder: i.placeholder }))
    );
    console.log('📝 表单字段:', JSON.stringify(inputs.slice(0, 10), null, 2));
    
    // 获取页面文本
    const bodyText = await page.$eval('body', el => el.innerText);
    console.log('📄 页面内容预览:', bodyText.substring(0, 500));
    
    await browser.close();
    console.log('✅ 完成');
}

registerGitHub().catch(console.error);
