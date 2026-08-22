/* =========================================================
   shincode - script.js

   担当する動き:
   01. スマホメニューの開閉
   02. スクロールに応じたヘッダーとナビの状態
   03. 要素をゆっくり表示する（控えめ）
   04. よくある質問の開閉
   05. お問い合わせフォームの入力チェック
   06. フッターの年号

   ※ 数値のカウントアップ演出は、根拠のない実績値を廃止したため削除しました。
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var MOBILE_QUERY = window.matchMedia('(max-width: 767px)');

  /* =======================================================
     01. スマホメニューの開閉
     ======================================================= */
  var hamburger = document.getElementById('hamburger');
  var nav = document.getElementById('nav');
  var lastFocused = null;

  function closeMenu(returnFocus) {
    if (!hamburger || !nav) return;
    if (!nav.classList.contains('is-open')) return;

    hamburger.classList.remove('is-open');
    nav.classList.remove('is-open');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-label', 'メニューを開く');
    document.body.classList.remove('is-locked');

    if (returnFocus && lastFocused) lastFocused.focus();
  }

  function openMenu() {
    if (!hamburger || !nav) return;
    lastFocused = document.activeElement;
    hamburger.classList.add('is-open');
    nav.classList.add('is-open');
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.setAttribute('aria-label', 'メニューを閉じる');
    document.body.classList.add('is-locked');

    var first = nav.querySelector('a');
    if (first) first.focus();
  }

  if (hamburger && nav) {
    hamburger.addEventListener('click', function () {
      if (nav.classList.contains('is-open')) closeMenu(true);
      else openMenu();
    });

    // メニュー内のリンクを押したら閉じる
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { closeMenu(false); });
    });

    // Escキーで閉じる
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu(true);
    });

    // メニューを開いたまま画面幅が広がった場合の後始末
    MOBILE_QUERY.addEventListener('change', function (e) {
      if (!e.matches) closeMenu(false);
    });
  }

  /* =======================================================
     02. スクロールに応じたヘッダーとナビの状態
     ======================================================= */
  var header = document.getElementById('header');
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__link'));
  var sections = navLinks
    .map(function (link) { return document.querySelector(link.getAttribute('href')); })
    .filter(Boolean);

  var ticking = false;

  function onScroll() {
    var y = window.pageYOffset || document.documentElement.scrollTop;

    if (header) header.classList.toggle('is-scrolled', y > 8);

    // 今見ているセクションのナビに印をつける
    var currentIndex = -1;
    sections.forEach(function (sec, i) {
      if (sec.getBoundingClientRect().top <= 140) currentIndex = i;
    });

    navLinks.forEach(function (link, i) {
      var isCurrent = (i === currentIndex);
      link.classList.toggle('is-active', isCurrent);
      if (isCurrent) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });

    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });

  onScroll();

  /* =======================================================
     03. 要素をゆっくり表示する（控えめ・時間差なし）
     ======================================================= */
  var revealItems = document.querySelectorAll('.reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -5% 0px' });

    revealItems.forEach(function (el) { revealObserver.observe(el); });
  }

  /* =======================================================
     04. よくある質問の開閉
     ======================================================= */
  var faqButtons = Array.prototype.slice.call(document.querySelectorAll('.faq__q'));

  function closeFaq(btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    btn.setAttribute('aria-expanded', 'false');
    if (panel) panel.style.maxHeight = null;
  }

  faqButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      var isOpen = btn.getAttribute('aria-expanded') === 'true';

      // 開いている他の項目は閉じる
      faqButtons.forEach(function (other) {
        if (other !== btn) closeFaq(other);
      });

      btn.setAttribute('aria-expanded', String(!isOpen));
      if (panel) panel.style.maxHeight = isOpen ? null : panel.scrollHeight + 'px';
    });
  });

  // 画面幅が変わったとき、開いている項目の高さを測り直す
  window.addEventListener('resize', function () {
    faqButtons.forEach(function (btn) {
      if (btn.getAttribute('aria-expanded') !== 'true') return;
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (panel) {
        panel.style.maxHeight = 'none';
        var h = panel.scrollHeight;
        panel.style.maxHeight = h + 'px';
      }
    });
  });

  /* =======================================================
     05. お問い合わせフォームの入力チェック
     ======================================================= */
  var form = document.getElementById('contactForm');
  var formStatus = document.getElementById('formStatus');

  function fieldOf(input) { return input.closest('.form__field'); }

  function showError(input, message) {
    var field = fieldOf(input);
    if (!field) return;
    field.classList.add('is-error');
    input.setAttribute('aria-invalid', 'true');
    var slot = field.querySelector('.form__error');
    if (slot) slot.textContent = message;
  }

  function clearError(input) {
    var field = fieldOf(input);
    if (!field) return;
    field.classList.remove('is-error');
    input.removeAttribute('aria-invalid');
    var slot = field.querySelector('.form__error');
    if (slot) slot.textContent = '';
  }

  function validateInput(input) {
    var value = (input.value || '').trim();

    if (input.type === 'checkbox') {
      if (input.required && !input.checked) {
        showError(input, '同意のチェックをお願いします。');
        return false;
      }
      clearError(input);
      return true;
    }

    if (input.required && value === '') {
      showError(input, input.tagName === 'SELECT' ? '選択をお願いします。' : '入力をお願いします。');
      return false;
    }

    if (input.type === 'email' && value !== '') {
      // 「文字＠文字．文字」の形かどうかだけを確認する簡易チェック
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        showError(input, 'メールアドレスの形式をご確認ください。');
        return false;
      }
    }

    clearError(input);
    return true;
  }

  if (form) {
    var targets = Array.prototype.slice.call(
      form.querySelectorAll('input, select, textarea')
    );

    // 一度エラーが出た項目は、直したらすぐ表示を消す
    targets.forEach(function (input) {
      var eventName = (input.type === 'checkbox' || input.tagName === 'SELECT') ? 'change' : 'blur';
      input.addEventListener(eventName, function () {
        var field = fieldOf(input);
        if (field && field.classList.contains('is-error')) validateInput(input);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var firstInvalid = null;
      targets.forEach(function (input) {
        if (!validateInput(input) && firstInvalid === null) firstInvalid = input;
      });

      if (firstInvalid) {
        if (formStatus) {
          formStatus.hidden = false;
          formStatus.textContent = '未入力の項目があります。赤く表示された箇所をご確認ください。';
        }
        firstInvalid.focus({ preventScroll: true });
        firstInvalid.scrollIntoView({
          behavior: reduceMotion ? 'auto' : 'smooth',
          block: 'center'
        });
        return;
      }

      /* ==== 送信（Netlify Forms 宛て） ====
         Netlify に置いたページから、フォームの内容をそのまま送ります。
         ローカルのファイルを直接開いた場合は届きません（公開後に動きます）。
      ==================================================== */
      var submitBtn = form.querySelector('button[type="submit"]');

      function setStatus(message) {
        if (!formStatus) return;
        formStatus.hidden = false;
        formStatus.textContent = message;
      }

      setStatus('送信しています。しばらくお待ちください。');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = '送信中…';
      }

      function restoreButton() {
        if (!submitBtn) return;
        submitBtn.disabled = false;
        submitBtn.textContent = 'この内容で送信する';
      }

      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      })
        .then(function (res) {
          if (!res.ok) throw new Error('status ' + res.status);

          setStatus('送信しました。1営業日以内にご返信します。');
          form.reset();
          restoreButton();
          if (formStatus) {
            formStatus.scrollIntoView({
              behavior: reduceMotion ? 'auto' : 'smooth',
              block: 'center'
            });
          }
        })
        .catch(function () {
          // 失敗を成功に見せない。入力内容は消さずに残す。
          setStatus('送信できませんでした。通信状況をご確認のうえ、もう一度お試しください。');
          restoreButton();
        });
    });
  }

  /* =======================================================
     06. フッターの年号
     ======================================================= */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());
});
