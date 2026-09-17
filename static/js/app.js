const hamburger = document.getElementById('hamburger');
const nav = document.querySelector('.nav');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  nav.classList.toggle('active');
});

// Mobile Submenu Toggles
const dropdownLinks = document.querySelectorAll('.nav li > a');

dropdownLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    // Only apply on mobile/tablet widths
    if (window.innerWidth <= 1024) {
      const submenu = link.nextElementSibling;

      if (submenu && submenu.tagName === 'UL') {
        e.preventDefault();
        const parentLi = link.parentElement;
        const opening = !submenu.classList.contains('active');

        submenu.classList.toggle('active');
        parentLi.classList.toggle('expanded', opening);

        // Rotate icon
        const icon = link.querySelector('i');
        if (icon) {
          icon.style.transform = opening ? 'rotate(180deg)' : 'rotate(0deg)';
        }
      }
    }
  });
});