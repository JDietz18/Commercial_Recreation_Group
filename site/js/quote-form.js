/*
 * CRG quote form: submits .crg-quote-form to its action with fetch and
 * shows the JSON reply in the form's [data-form-status] element.
 * Falls back to a normal POST if JavaScript is off.
 */
(function () {
  document.querySelectorAll('.crg-quote-form').forEach(function (form) {
    var status = form.querySelector('[data-form-status]');
    var button = form.querySelector('[type="submit"]');

    function show(kind, msg) {
      status.className = 'crg-form-status crg-form-status--' + kind;
      status.textContent = msg;
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
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data && data.status === 1) {
            show('ok', data.msg);
            form.reset();
          } else {
            show('error', (data && data.msg) || 'Something went wrong. Please try again.');
          }
        })
        .catch(function () {
          show('error', 'Your request could not be sent. Please check your connection, or call or email us directly.');
        })
        .then(function () {
          button.disabled = false;
          if (window.grecaptcha && form.querySelector('.g-recaptcha')) window.grecaptcha.reset();
        });
    });
  });
})();
