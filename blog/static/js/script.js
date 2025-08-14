/**
 * Toggle mobile navigation.
 */
export function initNavToggle(
  navToggleBtn = document.getElementById('nav-toggle'),
  navList = document.querySelector('.nav__list')
) {
  if (!navToggleBtn || !navList) return;

  // A11y wiring
  navToggleBtn.setAttribute('aria-expanded', 'false');
  navToggleBtn.setAttribute('aria-controls', 'primary-navigation');
  navList.id = navList.id || 'primary-navigation';
  navList.hidden = true;

  function closeNav() {
    navList.classList.remove('active');
    navToggleBtn.setAttribute('aria-expanded', 'false');
    navList.hidden = true;
  }
  function openNav() {
    navList.classList.add('active');
    navToggleBtn.setAttribute('aria-expanded', 'true');
    navList.hidden = false;
  }

  navToggleBtn.addEventListener('click', () => {
    const expanded = navToggleBtn.getAttribute('aria-expanded') === 'true';
    if (expanded) {
      closeNav();
    } else {
      openNav();
    }
  });

  // Close on Escape when open
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navToggleBtn.getAttribute('aria-expanded') === 'true') {
      closeNav();
      navToggleBtn.focus();
    }
  });
}

/**
 * Toggle light/dark theme.
 */
export function initThemeToggle(
  themeToggleBtn = document.getElementById('theme-toggle'),
  rootElement = document.documentElement
) {
  if (!themeToggleBtn) return;

  function applyTheme(theme) {
    rootElement.setAttribute('data-theme', theme);
    themeToggleBtn.textContent = theme === 'dark' ? '☀' : '☾';
    themeToggleBtn.setAttribute(
      'aria-label',
      `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`
    );
  }

  // storage helpers with safety
  const storage = {
    get(key) {
      try {
        return window.localStorage.getItem(key);
      } catch {
        return null;
      }
    },
    set(key, val) {
      try {
        window.localStorage.setItem(key, val);
      } catch {
        /* ignore */
      }
    },
    remove(key) {
      try {
        window.localStorage.removeItem(key);
      } catch {
        /* ignore */
      }
    },
  };

  const media = window.matchMedia
    ? window.matchMedia('(prefers-color-scheme: dark)')
    : { matches: false, addEventListener() {}, removeEventListener() {} };

  const storedTheme = storage.get('theme');
  const defaultTheme = storedTheme || (media.matches ? 'dark' : 'light');
  applyTheme(defaultTheme);

  themeToggleBtn.addEventListener('click', () => {
    const current = rootElement.getAttribute('data-theme') || 'light';
    const nextTheme = current === 'light' ? 'dark' : 'light';
    applyTheme(nextTheme);
    storage.set('theme', nextTheme); // user preference overrides system
  });

  // Track system changes only if user didn't set a manual preference
  const handleMediaChange = (e) => {
    if (!storage.get('theme')) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  };
  try {
    media.addEventListener('change', handleMediaChange);
  } catch {
    // Safari < 14 fallback
    media.addListener && media.addListener(handleMediaChange);
  }
}

// Hook into DOMContentLoaded for production use
if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    initNavToggle();
    initThemeToggle();
  });
}

/**
 * Flash toasts (close and auto-dismiss).
 */
(function initToasts() {
  const container = document.getElementById('flash-messages');
  if (!container) return;

  // Close on click (event delegation)
  container.addEventListener('click', (e) => {
    const btn = e.target.closest('.toast__close');
    if (!btn) return;
    const toast = btn.closest('.toast');
    if (toast) toast.remove();
  });

  // Auto-dismiss with pause-on-hover/focus
  const toasts = container.querySelectorAll('.toast');
  toasts.forEach((t, idx) => {
    let timeoutId;

    const startTimer = () => {
      // stagger by index to avoid simultaneous disappearance
      const delay = 4000 + idx * 250;
      timeoutId = window.setTimeout(() => {
        if (t && t.parentNode) t.remove();
      }, delay);
    };

    const clearTimer = () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
    };

    // start timer
    startTimer();

    // pause on hover or focus
    t.addEventListener('mouseenter', clearTimer);
    t.addEventListener('focusin', clearTimer);

    // resume on leave or blur
    t.addEventListener('mouseleave', startTimer);
    t.addEventListener('focusout', startTimer);
  });
})();

