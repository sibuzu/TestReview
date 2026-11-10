// Read-only verification of the actual local monitor after the 47-original goal.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../../..');
const {chromium} = require(path.join(root, '.cache/qa-tools/node_modules/playwright'));

(async () => {
  const browser = await chromium.launch({headless: true});
  const results = [], errors = [], cloudCalls = [];
  const screenshots = path.join(root, '.cache/intake-20261110');
  try {
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/.netlify/functions/**', route => {
      cloudCalls.push(1);
      return route.abort();
    });
    for (const width of [1440, 390]) {
      await page.setViewportSize({width, height: 1000});
      const response = await page.goto('http://127.0.0.1:8912/', {waitUntil: 'domcontentloaded'});
      assert.equal(response.status(), 200);
      await page.waitForFunction(() => document.querySelector('#comic-counts')
        ?.textContent.includes('932/932'));
      assert.equal(await page.locator('#comic-progress').isVisible(), false);
      assert.equal(await page.locator('#priority-source-card').isVisible(), false);
      assert.equal(await page.locator('#comic-rework').isVisible(), false);
      const activityTitle = await page.locator('#activity-title').innerText();
      assert.match(activityTitle, /7|932/);
      const api = await page.request.get('http://127.0.0.1:8912/api/status');
      assert.equal(api.status(), 200);
      const current = await api.json();
      assert.equal(current.comics.total, 932);
      assert.equal(current.comics.settled, 932);
      assert.equal(current.comics.remaining, 0);
      assert.equal(current.comics.percent, 100);
      assert.equal(current.activity.goalStatus, 'complete');
      assert.equal(current.summary.newSourcesPending, 0);
      const screenshot = path.join(screenshots, `monitor-final-${width}.png`);
      await page.screenshot({path: screenshot});
      results.push({width, activityTitle, screenshot: path.relative(root, screenshot),
        settled: current.comics.settled, total: current.comics.total,
        completedProgressSectionsHidden: true, pendingSources: current.summary.newSourcesPending,
        activeQuestions: current.comics.active});
    }
    assert.deepEqual(errors, []);
    assert.equal(cloudCalls.length, 0);
  } finally {
    await browser.close();
  }
  const result = {checkedAt: new Date().toISOString(), passed: true,
    scope: 'Local monitor completion state and hiding behavior; no account or mark APIs used.',
    pageErrors: errors, cloudApiRequests: cloudCalls.length, visualInspectionPending: true, results};
  fs.writeFileSync(path.join(root, 'docs/imports/new-gpt-20261110/monitor-validation.json'),
    JSON.stringify(result, null, 2) + '\n');
  console.log('PASS final monitor desktop/mobile state; view screenshots before visual sign-off.');
})().catch(error => { console.error(error); process.exitCode = 1; });
