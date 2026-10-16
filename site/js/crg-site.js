/*
 * CRG site helpers (runs after Intera's combining.js).
 */
(function () {
  // Add ?draft to any URL to outline placeholder copy that still needs CRG's review.
  if (/[?&]draft\b/.test(location.search)) document.documentElement.classList.add('crg-show-draft');

  // Project filter: Intera's masonry filter does the filtering; this keeps
  // the active style and pressed state in sync.
  document.querySelectorAll('.site-filters .filters').forEach(function (list) {
    list.addEventListener('click', function (e) {
      var item = e.target.closest('li');
      if (!item) return;
      e.preventDefault();
      list.querySelectorAll('li').forEach(function (li) {
        li.classList.toggle('active', li === item);
        li.querySelector('a').setAttribute('aria-pressed', String(li === item));
      });
    });
  });

  // Case-study videos: a plain link to Vimeo/YouTube until clicked, so nothing
  // loads from those sites (or sets cookies) unless the visitor asks for it.
  document.addEventListener('click', function (e) {
    var link = e.target.closest && e.target.closest('a.crg-video[data-embed]');
    if (!link || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault();
    var frame = document.createElement('iframe');
    frame.src = link.getAttribute('data-embed');
    frame.title = link.getAttribute('data-title') || 'Project video';
    frame.allow = 'autoplay; fullscreen; picture-in-picture';
    frame.allowFullscreen = true;
    var box = document.createElement('div');
    box.className = 'crg-video is-playing';
    box.appendChild(frame);
    link.replaceWith(box);
    frame.focus();
  });
})();
