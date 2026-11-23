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

  // Only fixed public choices and successful share operations are sent here.
  const eventNames = new Set(['select_filter', 'share']);
  const eventFields = new Set(['filter_name', 'filter_value', 'method', 'content_type', 'item_id']);
  window.minaTrack = (name, params = {}) => {
    if (!eventNames.has(name) || window['ga-disable-G-PT03XG7KQR']) return;
    try {
      const safe = {send_to:'G-PT03XG7KQR', page_location:'https://djnaoyaman.github.io/', page_referrer:''};
      for (const [key, value] of Object.entries(params)) {
        if (eventFields.has(key) && typeof value === 'string' && /^[a-z0-9_-]{1,60}$/.test(value)) safe[key] = value;
      }
      track('event', name, safe);
    } catch { /* Measurement must never interrupt the page. */ }
  };

  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin) return;
    const project = url.pathname.split('/')[1];
    if (project && /^[a-z0-9_-]+$/.test(project)) {
      if (!window['ga-disable-G-PT03XG7KQR']) track('event', 'creator_site_visit', {target_site: project, send_to:'G-PT03XG7KQR'});
    }
  });
})();

