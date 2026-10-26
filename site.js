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
      count.textContent = theme === 'all' ? `${projects.length} websites` : `${visible} / ${projects.length} websites`;
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
  const announce = message => {
    clearTimeout(announcement);
    status.textContent = '';
    announcement = setTimeout(() => { status.textContent = message; }, 30);
  };
  if (navigator.clipboard && window.isSecureContext && copyButton) {
    copyButton.hidden = false;
    copyButton.addEventListener('click', async () => {
      copyButton.disabled = true;
      try {
        await navigator.clipboard.writeText(canonical);
        announce('リンクをコピーしました。');
      } catch {
        announce(`コピーできませんでした。URLを選択してコピーしてください：${canonical}`);
      } finally { copyButton.disabled = false; }
    });
  }
  if (navigator.share && shareButton) {
    shareButton.hidden = false;
    shareButton.addEventListener('click', async () => {
      shareButton.disabled = true;
      // Do not leave a previous success/error visible if this share is cancelled.
      clearTimeout(announcement);
      status.textContent = '';
      try {
        await navigator.share({title:document.title,text:'音楽も、科学も、表現も、暮らしも。宮崎直哉のWebプロジェクト集。',url:canonical});
      } catch (error) {
        if (error?.name !== 'AbortError') announce('共有を開けませんでした。Xでシェア、またはリンクのコピーをご利用ください。');
      } finally { shareButton.disabled = false; }
    });
  }
})();
