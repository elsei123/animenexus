/**
 * Toggle mobile navigation.
 */
export function initNavToggle(
  navToggleBtn = document.getElementById('nav-toggle'),
  navList = document.querySelector('.nav__list')
) {
  if (!navToggleBtn || !navList) return;
  navToggleBtn.setAttribute('aria-expanded', 'false');
  navToggleBtn.addEventListener('click', () => {
    const expanded = navToggleBtn.getAttribute('aria-expanded') === 'true';
    navList.classList.toggle('active');
    navToggleBtn.setAttribute('aria-expanded', String(!expanded));
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

  const storedTheme = localStorage.getItem('theme');
  const prefersDark =
    window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const defaultTheme = storedTheme || (prefersDark ? 'dark' : 'light');
  applyTheme(defaultTheme);

  themeToggleBtn.addEventListener('click', () => {
    const current = rootElement.getAttribute('data-theme') || 'light';
    const nextTheme = current === 'light' ? 'dark' : 'light';
    applyTheme(nextTheme);
    localStorage.setItem('theme', nextTheme);
  });
}

// Hook into DOMContentLoaded for production use
if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    initNavToggle();
    initThemeToggle();
  });
}
