document.addEventListener('DOMContentLoaded', () => {
  // Mobile navigation toggle
  const navToggleBtn = document.getElementById('nav-toggle');
  const navList = document.querySelector('.nav__list');

  function initNavToggle() {
    if (!navToggleBtn || !navList) return;
    navToggleBtn.setAttribute('aria-expanded', 'false');
    navToggleBtn.addEventListener('click', () => {
      const expanded = navToggleBtn.getAttribute('aria-expanded') === 'true';
      navList.classList.toggle('active');
      navToggleBtn.setAttribute('aria-expanded', String(!expanded));
    });
  }

  // Theme toggle (dark/light mode)
  const themeToggleBtn = document.getElementById('theme-toggle');
  const rootElement = document.documentElement;

  function applyTheme(theme) {
    rootElement.setAttribute('data-theme', theme);
    if (themeToggleBtn) {
      themeToggleBtn.textContent = theme === 'dark' ? '☀' : '☾';
      themeToggleBtn.setAttribute(
        'aria-label',
        `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`
      );
    }
  }

  function initThemeToggle() {
    if (!themeToggleBtn) return;
    const storedTheme = localStorage.getItem('theme');
    const prefersDark =
      window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches;
    const defaultTheme = storedTheme || (prefersDark ? 'dark' : 'light');
    applyTheme(defaultTheme);

    themeToggleBtn.addEventListener('click', () => {
      const current = rootElement.getAttribute('data-theme') || 'light';
      const nextTheme = current === 'light' ? 'dark' : 'light';
      applyTheme(nextTheme);
      localStorage.setItem('theme', nextTheme);
    });
  }

  initNavToggle();
  initThemeToggle();
});
