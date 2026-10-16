/*
 * CRG quote form: submits .crg-quote-form to its action with fetch and
 * shows the JSON reply in the form's [data-form-status] element.
 *
 * If the server can't take the request (static hosting such as GitHub
 * Pages has no PHP, or the network fails), the visitor's details are kept
 * and they get a one-click email to CRG pre-filled with everything they
 * typed, plus the phone number. Falls back to a normal POST without JS.
 */
(function () {
  function fieldText(form) {
    var lines = [];
    form.querySelectorAll('.crg-field').forEach(function (field) {
      var label = field.querySelector('label');
      var input = field.querySelector('input, select, textarea');
      if (!label || !input || !input.value.trim()) return;
      var name = label.textContent.replace(/\*/g, '').trim();
      lines.push(name + ': ' + input.value.trim());
    });
    return lines.join('\n');
  }

  function mailtoFor(form) {
    var email = form.getAttribute('data-fallback-email');
    var org = form.querySelector('[name="organization"]');
    var who = form.querySelector('[name="name"]');
    var subject = 'Quote request' + ((org && org.value.trim()) || (who && who.value.trim())
      ? ': ' + ((org && org.value.trim()) || who.value.trim()) : '');
    var body = fieldText(form);
    // Keep the link within what mail apps reliably accept.
    if (body.length > 1600) body = body.slice(0, 1600) + '…';
    return 'mailto:' + email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  document.querySelectorAll('.crg-quote-form').forEach(function (form) {
    var status = form.querySelector('[data-form-status]');
    var button = form.querySelector('[type="submit"]');

    function show(kind, msg) {
      status.className = 'crg-form-status crg-form-status--' + kind;
      status.textContent = msg;
    }

    function showFallback() {
      var phone = form.getAttribute('data-fallback-phone');
      status.className = 'crg-form-status crg-form-status--fallback';
      status.textContent = '';
      var p = document.createElement('span');
      p.textContent = 'We couldn’t send this online, but your details are still here. Send them by email in one click, or call us.';
      var actions = document.createElement('span');
      actions.className = 'crg-form-fallback';
      var mail = document.createElement('a');
      mail.className = 'crg-btn crg-btn--primary';
      mail.href = mailtoFor(form);
      mail.textContent = 'Email this request';
      var tel = document.createElement('a');
      tel.className = 'crg-btn crg-btn--outline';
      tel.href = 'tel:' + phone.replace(/[^\d+]/g, '');
      tel.textContent = 'Call ' + phone;
      actions.appendChild(mail);
      actions.appendChild(tel);
      status.appendChild(p);
      status.appendChild(actions);
      mail.focus();
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      button.disabled = true;
      show('pending', 'Sending…');

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          var type = res.headers.get('content-type') || '';
          if (!res.ok || type.indexOf('json') === -1) throw new Error('unavailable');
          return res.json();
        })
        .then(function (data) {
          if (data && data.fallback) {
            showFallback();
          } else if (data && data.status === 1) {
            show('ok', data.msg);
            form.reset();
          } else if (data && data.msg) {
            show('error', data.msg);
          } else {
            showFallback();
          }
        })
        .catch(showFallback)
        .then(function () {
          button.disabled = false;
          if (window.grecaptcha && form.querySelector('.g-recaptcha')) window.grecaptcha.reset();
        });
    });
  });
})();
