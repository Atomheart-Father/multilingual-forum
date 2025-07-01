#!/usr/bin/env node
/**
 * 🧪 多语言论坛部署测试脚本
 * 验证Vercel前端和Render后端的连接
 */

const https = require('https');
const http = require('http');

// 测试配置
const TESTS = {
  render_backend: {
    name: '🔧 Render后端API',
    url: 'https://multilingual-forum-api.onrender.com/api/health',
    timeout: 30000
  },
  vercel_frontend: {
    name: '🎨 Vercel前端',
    url: 'https://multilingual-forum.vercel.app',
    timeout: 10000
  }
};

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// HTTP请求封装
function makeRequest(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const isHttps = url.startsWith('https');
    const client = isHttps ? https : http;
    
    const req = client.get(url, { timeout }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    req.on('error', reject);
  });
}

// 测试后端API
async function testBackend() {
  log('\n🔧 测试Render后端...', 'blue');
  
  try {
    const response = await makeRequest(TESTS.render_backend.url, TESTS.render_backend.timeout);
    
    if (response.statusCode === 200) {
      const data = JSON.parse(response.body);
      log('✅ 后端健康检查通过', 'green');
      log(`   状态: ${data.status}`, 'cyan');
      log(`   版本: ${data.version}`, 'cyan');
      log(`   Python版本: ${data.python_version}`, 'cyan');
      log(`   帖子数量: ${data.posts_count}`, 'cyan');
      return true;
    } else {
      log(`❌ 后端响应错误: ${response.statusCode}`, 'red');
      return false;
    }
  } catch (error) {
    log(`❌ 后端连接失败: ${error.message}`, 'red');
    return false;
  }
}

// 测试前端
async function testFrontend() {
  log('\n🎨 测试Vercel前端...', 'blue');
  
  try {
    const response = await makeRequest(TESTS.vercel_frontend.url, TESTS.vercel_frontend.timeout);
    
    if (response.statusCode === 200) {
      log('✅ 前端访问正常', 'green');
      log(`   状态码: ${response.statusCode}`, 'cyan');
      
      // 检查是否包含React应用标识
      if (response.body.includes('root') || response.body.includes('react')) {
        log('   ✓ React应用加载成功', 'cyan');
      }
      
      return true;
    } else {
      log(`❌ 前端响应错误: ${response.statusCode}`, 'red');
      return false;
    }
  } catch (error) {
    log(`❌ 前端连接失败: ${error.message}`, 'red');
    return false;
  }
}

// 测试API端点
async function testAPIEndpoints() {
  log('\n🌐 测试API端点...', 'blue');
  
  const endpoints = [
    { name: '获取帖子', path: '/api/posts/' },
    { name: '支持语言', path: '/api/translate/languages' }
  ];
  
  let passedTests = 0;
  
  for (const endpoint of endpoints) {
    try {
      const url = `https://multilingual-forum-api.onrender.com${endpoint.path}`;
      const response = await makeRequest(url, 15000);
      
      if (response.statusCode === 200) {
        log(`   ✅ ${endpoint.name}: OK`, 'green');
        passedTests++;
      } else {
        log(`   ❌ ${endpoint.name}: ${response.statusCode}`, 'red');
      }
    } catch (error) {
      log(`   ❌ ${endpoint.name}: ${error.message}`, 'red');
    }
  }
  
  return passedTests === endpoints.length;
}

// 主测试函数
async function runTests() {
  log('🌍 多语言论坛部署测试开始...', 'yellow');
  log('=' .repeat(50), 'yellow');
  
  const results = {
    backend: false,
    frontend: false,
    api: false
  };
  
  // 测试后端
  results.backend = await testBackend();
  
  // 测试前端
  results.frontend = await testFrontend();
  
  // 测试API端点
  if (results.backend) {
    results.api = await testAPIEndpoints();
  }
  
  // 输出结果
  log('\n📊 测试结果汇总:', 'yellow');
  log('=' .repeat(50), 'yellow');
  
  log(`🔧 Render后端: ${results.backend ? '✅ 正常' : '❌ 异常'}`, results.backend ? 'green' : 'red');
  log(`🎨 Vercel前端: ${results.frontend ? '✅ 正常' : '❌ 异常'}`, results.frontend ? 'green' : 'red');
  log(`🌐 API端点: ${results.api ? '✅ 正常' : '❌ 异常'}`, results.api ? 'green' : 'red');
  
  // 总结
  const allPassed = Object.values(results).every(result => result);
  
  if (allPassed) {
    log('\n🎉 所有测试通过！前后端协同正常工作', 'green');
    log('👉 你可以开始使用论坛了:', 'cyan');
    log('   前端: https://multilingual-forum.vercel.app', 'cyan');
    log('   后端: https://multilingual-forum-api.onrender.com', 'cyan');
  } else {
    log('\n⚠️  部分测试失败，请检查以下问题:', 'yellow');
    if (!results.backend) log('   - Render后端可能未正常启动', 'red');
    if (!results.frontend) log('   - Vercel前端可能未正确部署', 'red');
    if (!results.api) log('   - API端点可能存在问题', 'red');
  }
  
  process.exit(allPassed ? 0 : 1);
}

// 运行测试
if (require.main === module) {
  runTests().catch(error => {
    log(`💥 测试过程发生错误: ${error.message}`, 'red');
    process.exit(1);
  });
}

module.exports = { runTests, testBackend, testFrontend }; 