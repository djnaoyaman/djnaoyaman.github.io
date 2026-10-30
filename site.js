'use strict';
(() => {
  const canonical = 'https://djnaoyaman.github.io/';
  const filters = document.querySelector('.project-filter');
  if (filters) {
    const buttons = [...filters.querySelectorAll('button[data-theme]')];
    const projects = [...document.querySelectorAll('.project')];
    const count = document.querySelector('#project-count');
    const valid = new Set(buttons.map(button => button.dataset.theme));
    const readTheme = () => new URL(location.href).searchParams.get('theme') || 'all';
    const apply = theme => {
      if (!valid.has(theme)) theme = 'all';
      let visible = 0;
      projects.forEach(project => {
        project.hidden = theme !== 'all' && project.dataset.theme !== theme;
        if (!project.hidden) visible++;
      });
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.theme === theme)));
      count.textContent = theme === 'all' ? `全${projects.length}サイト` : `${projects.length}サイト中${visible}サイトを表示`;
      count.setAttribute('aria-label', theme === 'all' ? `全${projects.length}件` : `${projects.length}件中${visible}件を表示`);
    };
    // Counts come from the actual cards, so adding a work cannot leave stale badges.
    buttons.forEach(button => {
      button.querySelector('span').textContent = projects.filter(project => button.dataset.theme === 'all' || project.dataset.theme === button.dataset.theme).length;
      button.addEventListener('click', () => {
        const url = new URL(location.href);
        const theme = button.dataset.theme;
        if (theme === 'all') url.searchParams.delete('theme');
        else url.searchParams.set('theme', theme);
        if (url.href !== location.href) {
          try { history.pushState(null, '', url); } catch { /* Filtering remains available if history is restricted. */ }
        }
        apply(theme);
      });
    });
    apply(readTheme());
    filters.hidden = false;
    window.addEventListener('popstate', () => apply(readTheme()));
  }

  if ('IntersectionObserver' in window) {
    const links = [...document.querySelectorAll('nav a[href^="#"]')];
    const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
    const visible = new Set();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? visible.add(entry.target.id) : visible.delete(entry.target.id));
      const current = sections.find(section => visible.has(section.id));
      links.forEach(link => {
        if (current && link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-10% 0px -45% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
  }

  const copyButton = document.querySelector('#copy-link');
  const shareButton = document.querySelector('#native-share');
  const status = document.querySelector('#share-status');
  if (!status) return;
  let announcement;
  let operation = 0;
  let copyOperation = 0, shareOperation = 0;
  const announce = message => {
    clearTimeout(announcement);
    status.textContent = '';
    announcement = setTimeout(() => { status.textContent = message; }, 30);
  };
  window.addEventListener('pageshow', event => {
    if (!event.persisted) return;
    operation++;
    copyOperation = shareOperation = 0;
    clearTimeout(announcement);
    status.textContent = '';
    if (copyButton) copyButton.disabled = false;
    if (shareButton) shareButton.disabled = false;
  });
  if (navigator.clipboard && window.isSecureContext && copyButton) {
    copyButton.hidden = false;
    copyButton.addEventListener('click', async () => {
      const ticket = copyOperation = ++operation;
      copyButton.disabled = true;
      try {
        await navigator.clipboard.writeText(canonical);
        if (ticket === operation) announce('リンクをコピーしました。');
      } catch {
        if (ticket === operation) announce(`コピーできませんでした。次のURLを選択してコピーしてください：${canonical}`);
      } finally { if (copyOperation === ticket) copyButton.disabled = false; }
    });
  }
  if (navigator.share && shareButton) {
    shareButton.hidden = false;
    shareButton.addEventListener('click', async () => {
      const ticket = shareOperation = ++operation;
      shareButton.disabled = true;
      // Do not leave a previous success/error visible if this share is cancelled.
      clearTimeout(announcement);
      status.textContent = '';
      try {
        await navigator.share({title:document.title,text:'ずーっと、あれも、これも。音楽、表現、自然と文化、暮らしと学び。宮崎直哉のWebプロジェクト集。',url:canonical});
      } catch (error) {
        if (ticket === operation && error?.name !== 'AbortError') announce('共有メニューを開けませんでした。「Xでシェア」または「リンクをコピー」をお試しください。');
      } finally { if (shareOperation === ticket) shareButton.disabled = false; }
    });
  }
})();
