'use strict';
(() => {
  if (window.__minaAnalyticsStarted || !document.querySelector('script[data-mina-ga]')) return;
  window.__minaAnalyticsStarted = true;
  window.dataLayer = window.dataLayer || [];
  function track() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || track;
  track('js', new Date());

  const isNotFound = !!document.querySelector('script[data-mina-not-found]');
  // A missing URL can contain visitor-supplied text; keep its measurement canonical.
  const options = isNotFound
    ? {page_location: 'https://djnaoyaman.github.io/404.html', page_referrer: ''}
    : {};
  track('config', 'G-PT03XG7KQR', options);

  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin) return;
    const project = url.pathname.split('/')[1];
    if (project && /^[a-z0-9_-]+$/.test(project)) {
      track('event', 'creator_site_visit', {target_site: project});
    }
  });
})();
