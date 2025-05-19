/**
 * @jest-environment jsdom
 */

import '@testing-library/jest-dom';
import { initNavToggle, initThemeToggle } from '../script';

describe('initNavToggle', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <button id="nav-toggle" aria-expanded="false"></button>
      <ul class="nav__list"></ul>
    `;
  });

  test('toggles nav list and aria-expanded attribute', () => {
    const btn = document.getElementById('nav-toggle');
    const list = document.querySelector('.nav__list');

    initNavToggle(btn, list);

    expect(btn).toHaveAttribute('aria-expanded', 'false');
    expect(list).not.toHaveClass('active');

    btn.click();
    expect(btn).toHaveAttribute('aria-expanded', 'true');
    expect(list).toHaveClass('active');

    btn.click();
    expect(btn).toHaveAttribute('aria-expanded', 'false');
    expect(list).not.toHaveClass('active');
  });
});

describe('initThemeToggle', () => {
  beforeEach(() => {
    document.body.innerHTML = `<button id="theme-toggle"></button>`;
    localStorage.clear();
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: (query) => ({
        matches: false,
        media: query,
        addListener: () => {},
        removeListener: () => {},
      }),
    });
  });

  test('applies default light theme and toggles to dark', () => {
    const btn = document.getElementById('theme-toggle');
    initThemeToggle(btn, document.documentElement);

    expect(document.documentElement).toHaveAttribute('data-theme', 'light');
    expect(btn.textContent).toBe('☾');
    expect(btn).toHaveAttribute('aria-label', 'Switch to dark mode');

    btn.click();
    expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
    expect(btn.textContent).toBe('☀');
    expect(btn).toHaveAttribute('aria-label', 'Switch to light mode');
    expect(localStorage.getItem('theme')).toBe('dark');
  });
});
