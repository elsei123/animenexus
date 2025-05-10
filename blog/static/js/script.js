document.addEventListener('DOMContentLoaded', () => {
    // Menu toggle (mobile)
const toggleButton = document.getElementById('nav-toggle');
const navigationList = document.querySelector('.nav__list');

toggleButton.addEventListener('click', () => {
  navigationList.classList.toggle('active');
});

  
// Theme toggle (dark/light mode)
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;
const savedTheme = localStorage.getItem('theme');
  
  if (savedTheme) {
    html.setAttribute('data-theme', savedTheme);
    themeToggle.textContent = savedTheme === 'dark' ? '☀' : '☾';
  }
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    themeToggle.textContent = newTheme === 'dark' ? '☀' : '☾';
    });
  }
});
  