const translations = {
  en: {
    title: 'SantaCode 2025',
    subtitle: "> Programmer's Secret Santa Event initialized...",
    mission_title: '🎯 The Mission',
    mission_desc_1: "Welcome to the Programmer's Secret Santa!",
    mission_desc_2: 'Your mission is to write a program that prints a **Christmas tree** to the screen.',
    mission_desc_3:
      'After the event, the system will swap code snippets. You will receive a tree planted by a secret santa in your terminal!',
    rules_title: '⚠️ System Constraints',
    rules_desc: 'To ensure safety, we strictly enforce:',
    rule_1: '<strong>No Internet</strong>: Offline environment.',
    rule_2: '<strong>Std Lib Only</strong>: No third-party packages.',
    rule_3: '<strong>Timeout</strong>: Max 5 seconds execution.',
    rule_4: '<strong>Output</strong>: Print to stdout.',
    rule_5: '<strong>ID Match</strong>: Folder name must match your GitHub ID.',
    rule_6: 'Please comply with the <a href="https://www.facebook.com/groups/GDGKaohsiung/permalink/3401057450144799/" target="_blank">Code of Conduct (CoC)</a>. Violations will result in blacklisting.',
    join_title: '🚀 How to Join',
    live_event_info: 'We will be holding SantaCode 2025 live at Developer Cafe on 12/30. Welcome to join us! For more details, please check the <a href="https://community-card.org/2026/calendar.html" target="_blank">Kaohsiung Community Calendar</a>',
    step_1_title: 'Fork Repo',
    step_1_desc: '<a href="https://github.com/gdg-kh/SantaCode" target="_blank">Fork this project</a> to your GitHub.',
    step_2_title: 'Create Directory',
    step_2_desc: 'Create a folder `submissions/YOUR_GitHub_ID/`.',
    step_3_title: 'Write Code',
    step_3_desc: 'Place your code (e.g., `tree.py`). You can check <a href="https://github.com/gdg-kh/SantaCode/tree/master/submissions/example-santa" target="_blank">multi-language examples here</a>.',
    step_4_title: 'Pull Request',
    step_4_desc: 'Submit PR. Wait for Green Check ✅.',
    step_5_title: '📬 Watch Repository (Important!)',
    step_5_desc: 'Click the <strong>Watch</strong> button at the top-right > Choose <strong>Custom</strong> > Check <strong>Issues ✅</strong><br/>When the exchange completes, the system will automatically create an Issue announcement, and you will be notified!<br/><em style="color: #ff6b6b;">⚠️ If you don\'t Watch, you won\'t receive notifications!</em>',
    exchange_title: '🎁 Exchange Mechanism',
    exchange_desc_1: 'After the deadline, the admin will trigger the automatic exchange system, which will randomly pair all participants.',
    exchange_desc_2: '<strong>Important:</strong> To avoid spamming with mass @mentions (which may be considered abuse by GitHub), we use an <strong>automatic Issue announcement</strong> mechanism. Please complete <strong>Step 5 (Watch Repository)</strong> above to ensure you receive notifications.',
    exchange_result: '🎅 After the exchange is complete, a gift code from a mysterious Santa will appear in your <code>submissions/YOUR_ID/</code> folder!',
    runtimes_title: '💾 Supported Runtimes',
    footer_status: 'Status: WAITING_FOR_SUBMISSIONS',
      gift_count_msg: '🎁 Look who sent a surprise! <strong>{count}</strong> exchange gifts collected so far.',
  },
  'zh-TW': {
    title: 'SantaCode 2025',
    subtitle: '> 工程師的交換禮物活動初始化中...',
    mission_title: '🎯 任務目標',
    mission_desc_1: '歡迎來到工程師專屬的交換禮物活動！',
    mission_desc_2: '你的任務是寫一個程式，執行後在螢幕上印出一棵 **聖誕樹**。',
    mission_desc_3: '活動結束後，系統會亂數配對。你會收到某個神秘人寫的程式，在你的終端機裡種下一棵樹！',
    rules_title: '⚠️ 系統限制 (規則)',
    rules_desc: '為了安全，我們嚴格執行以下限制：',
    rule_1: '<strong>無網路</strong>: 執行環境完全斷網。',
    rule_2: '<strong>限標準庫</strong>: 禁止第三方套件 (No pip/npm install)。',
    rule_3: '<strong>執行限時</strong>: 必須在 5 秒內跑完。',
    rule_4: '<strong>標準輸出</strong>: 請將結果印在 stdout。',
    rule_5: '<strong>一人一交</strong>: 資料夾名稱必須與 GitHub ID 完全一致。',
    rule_6: '請遵守<a href="https://www.facebook.com/groups/GDGKaohsiung/permalink/3401057450144799/" target="_blank">行為準則 COC</a>，違反者將會進入黑名單。',
    join_title: '🚀 如何參加',
    live_event_info: '我們在 12/30 的開發者 Cafe 進行現場的 SantaCode 2025，歡迎一起參加，詳細資訊請看<a href="https://community-card.org/2026/calendar.html" target="_blank">高雄社群月曆</a>',
    step_1_title: 'Fork 專案',
    step_1_desc: '<a href="https://github.com/gdg-kh/SantaCode" target="_blank">將本專案 Fork 到你的 GitHub。</a>',
    step_2_title: '建立目錄',
    step_2_desc: '建立資料夾 `submissions/你的 GitHub ID/`。',
    step_3_title: '撰寫程式',
    step_3_desc: '放入你的程式碼 (如 `tree.py`)。<a href="https://github.com/gdg-kh/SantaCode/tree/master/submissions/example-santa" target="_blank">參考多語言範例檔</a>。',
    step_4_title: '提交 PR',
    step_4_desc: '發送 Pull Request 等待綠勾勾 ✅。',
    step_5_title: '📬 Watch Repository (重要！)',
    step_5_desc: '點擊專案右上角的 <strong>Watch</strong> 按鈕 > 選擇 <strong>Custom</strong> > 勾選 <strong>Issues ✅</strong><br/>當交換完成時，系統會自動創建 Issue 公告，你將收到通知！<br/><em style="color: #ff6b6b;">⚠️ 不 Watch 就收不到通知哦！</em>',
    exchange_title: '🎁 交換機制說明',
    exchange_desc_1: '活動截止後，管理員會觸發自動交換系統，系統將隨機配對所有參與者。',
    exchange_desc_2: '<strong>重要：</strong>為了避免大量 @mention 造成困擾（可能被 GitHub 視為濫用），我們使用 <strong>自動 Issue 公告</strong>機制。請務必完成上方 <strong>步驟 5 (Watch Repository)</strong> 以接收通知。',
    exchange_result: '🎅 交換完成後，你的 <code>submissions/你的ID/</code> 資料夾中會出現來自神秘聖誕老人的禮物程式碼！',
    runtimes_title: '💾 支援語言環境',
    footer_status: '狀態: 等待投稿中',
      gift_count_msg: '🎁 看看是誰送來了驚喜？目前已累積 <strong>{count}</strong> 份交換禮物',
  },
  ja: {
    title: 'SantaCode 2025',
    subtitle: '> プログラマーのシークレットサンタ、起動中...',
    mission_title: '🎯 ミッション',
    mission_desc_1: 'プログラマーのためのプレゼント交換へようこそ！',
    mission_desc_2: 'あなたの任務は、実行すると画面に **クリスマスツリー** を表示するプログラムを書くことです。',
    mission_desc_3:
      'イベント終了後、システムがランダムにコードを交換します。あなたのターミナルに誰かのツリーが植えられます！',
    rules_title: '⚠️ システム制約 (ルール)',
    rules_desc: '安全のため、以下の制限を厳守してください：',
    rule_1: '<strong>オフライン</strong>: 実行環境はネット接続なし。',
    rule_2: '<strong>標準ライブラリのみ</strong>: 外部パッケージ禁止。',
    rule_3: '<strong>タイムアウト</strong>: 実行時間は5秒以内。',
    rule_4: '<strong>出力</strong>: 結果は標準出力 (stdout) へ。',
    rule_5: '<strong>一人一回</strong>: フォルダ名はGitHub IDと一致必須。',
    rule_6: '行動規範（<a href="https://www.facebook.com/groups/GDGKaohsiung/permalink/3401057450144799/" target="_blank">CoC</a>）を遵守してください。違反者はブラックリストに登録されます。',
    join_title: '🚀 参加方法',
    live_event_info: '12/30 の開発者カフェで SantaCode 2025 を現地開催します。ぜひご参加ください。詳細は<a href="https://community-card.org/2026/calendar.html" target="_blank">高雄コミュニティカレンダー</a>をご確認ください',
    step_1_title: 'リポジトリをFork',
    step_1_desc: '<a href="https://github.com/gdg-kh/SantaCode" target="_blank">このプロジェクトを自分のGitHubにForkします。</a>',
    step_2_title: 'フォルダ作成',
    step_2_desc: '`submissions/あなたの GitHub ID/` フォルダを作成。',
    step_3_title: 'コード作成',
    step_3_desc: 'プログラムを配置 (例: `tree.py`)。<a href="https://github.com/gdg-kh/SantaCode/tree/master/submissions/example-santa" target="_blank">多言語の例はこちら</a>。',
    step_4_title: 'プルリクエスト',
    step_4_desc: 'PRを送信し、緑のチェック ✅ を待つ。',
    step_5_title: '📬 リポジトリをWatch（重要！）',
    step_5_desc: 'プロジェクト右上の <strong>Watch</strong> ボタンをクリック > <strong>Custom</strong> を選択 > <strong>Issues ✅</strong> にチェック<br/>交換が完了すると、システムが自動的にIssue通知を作成します！<br/><em style="color: #ff6b6b;">⚠️ Watchしないと通知を受け取れません！</em>',
    exchange_title: '🎁 交換メカニズム',
    exchange_desc_1: '締め切り後、管理者が自動交換システムを起動し、すべての参加者をランダムにペアリングします。',
    exchange_desc_2: '<strong>重要：</strong>大量の @mention によるスパム（GitHubから悪用と見なされる可能性があります）を避けるため、<strong>自動Issue通知</strong>メカニズムを使用します。通知を受け取るため、必ず上記の <strong>Step 5 (Watch Repository)</strong> を完了してください。',
    exchange_result: '🎅 交換完了後、あなたの <code>submissions/あなたのID/</code> フォルダに謎のサンタからのギフトコードが現れます！',
    runtimes_title: '💾 対応ランタイム',
    footer_status: 'ステータス: 投稿待ち',
      gift_count_msg: '🎁 誰がサプライズを届けたか見てみよう！現在 <strong>{count}</strong> 個のギフトが集まりました',
  },
};

let currentGiftCount = null;

function updateGiftCountDisplay(lang) {
  const counterEl = document.getElementById('gift-counter');
  const statusEl = document.getElementById('event-status');
  if (!counterEl || !statusEl || currentGiftCount === null) return;
  
  if (currentGiftCount > 0) {
    const msgTemplate = translations[lang]['gift_count_msg'];
    if (msgTemplate) {
      counterEl.innerHTML = msgTemplate.replace('{count}', currentGiftCount);
      counterEl.style.display = 'inline';
      statusEl.style.display = 'none';
    }
  } else {
    counterEl.style.display = 'none';
    statusEl.style.display = 'inline';
  }
}

async function fetchGiftCount() {
  try {
    const response = await fetch('https://api.github.com/repos/gdg-kh/SantaCode/contents/submissions');
    if (!response.ok) return;
    
    const data = await response.json();
    // Filter out 'example-santa' and non-directory items
      const submitters = data.filter(item => item.type === 'dir' && item.name !== 'example-santa');

      currentGiftCount = submitters.length;
    
    // Update display with current active language
    const currentLang = document.querySelector('.lang-btn.active')?.dataset.lang || 'en';
    updateGiftCountDisplay(currentLang);

      // Update submitter list
      const listEl = document.getElementById('submitter-list');
      if (listEl) {
          listEl.innerHTML = submitters.map(s => `
        <div class="gift-card" title="Gift from ${s.name}">
          <span class="icon">🎁</span>
          <span class="name">${s.name}</span>
        </div>
      `).join('');
      }
    
  } catch (e) {
    console.log('Failed to fetch gift count', e);
  }
}

function setLanguage(lang) {
  if (!translations[lang]) return;

  // Update all elements with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const key = element.getAttribute('data-i18n');
    if (translations[lang][key]) {
      element.innerHTML = translations[lang][key];
    }
  });

  // Update gift counter if count is available
  updateGiftCountDisplay(lang);

  // Update buttons state
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.remove('active');
    if (btn.dataset.lang === lang) {
      btn.classList.add('active');
    }
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  let defaultLang = 'en';

  // Check localStorage first
  const savedLang = localStorage.getItem('santacode_lang');

  if (savedLang) {
    defaultLang = savedLang;
  } else {
    // Detect browser language
    const browserLang = navigator.language || navigator.userLanguage;
    const langCode = browserLang.toLowerCase().split('-')[0]; // Get 'zh', 'ja', 'en'

    if (langCode === 'zh') {
      defaultLang = 'zh-TW';
    } else if (langCode === 'ja') {
      defaultLang = 'ja';
    }
  }

  setLanguage(defaultLang);
  fetchGiftCount(); // Fetch count on load

  document.querySelectorAll('.lang-btn').forEach((btn) => {

    btn.addEventListener('click', (e) => {
      const selectedLang = e.target.dataset.lang;
      setLanguage(selectedLang);
      // Only save when user explicitly clicks
      localStorage.setItem('santacode_lang', selectedLang);
    });
  });
});
