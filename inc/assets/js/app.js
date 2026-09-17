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
      const icon = link.querySelector('i');

      if (submenu && submenu.tagName === 'UL' && icon) {
        // Toggle submenu only if the arrow icon itself is clicked
        if (e.target === icon || icon.contains(e.target)) {
          e.preventDefault();
          const parentLi = link.parentElement;
          const opening = !submenu.classList.contains('active');

          submenu.classList.toggle('active');
          parentLi.classList.toggle('expanded', opening);

          // Rotate icon
          icon.style.transform = opening ? 'rotate(180deg)' : 'rotate(0deg)';
        }
      }
    }
  });
});

// Reviews Tab Switching
const tabItems = document.querySelectorAll('.tab-item');
const tabContents = document.querySelectorAll('.tab-content');

tabItems.forEach(tab => {
  tab.addEventListener('click', () => {
    const target = tab.getAttribute('data-tab');

    // Remove active class from all tabs and contents
    tabItems.forEach(item => item.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));

    // Add active class to current tab and content
    tab.classList.add('active');
    document.getElementById(target).classList.add('active');
  });
});

// Burger Swiper Initialization
if (document.querySelector('.burger-swiper')) {
  const burgerSwiper = new Swiper('.burger-swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView: 1,
    spaceBetween: 0, // No space between slides like the screenshot
    autoHeight: true,

    // Responsive breakpoints
    breakpoints: {
      // when window width is >= 576px
      576: {
        slidesPerView: 2,
      },
      // when window width is >= 768px
      768: {
        slidesPerView: 3,
      },
      // when window width is >= 1024px
      1024: {
        slidesPerView: 4,
      }
    },

    // Pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
}

// Hero Swiper Initialization
if (document.querySelector('.hero-swiper')) {
  const heroSwiper = new Swiper('.hero-swiper', {
    loop: true,
    speed: 1000,
    autoplay: {
      delay: 6000,
      disableOnInteraction: false,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  });
}

// Testimonial Swiper Initialization
if (document.querySelector('.testimonial-swiper')) {
  const testimonialSwiper = new Swiper('.testimonial-swiper', {
    loop: true,
    speed: 800,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
}

// ===== Mobile Sticky ORDER Button — Stick to bottom, stop at footer =====
(function () {
  const mobileOrder = document.querySelector('.mobile-order');
  const footer = document.querySelector('.footer');

  if (!mobileOrder || !footer) return;

  function updateStickyOrder() {
    // Only active on mobile widths
    if (window.innerWidth > 767) {
      mobileOrder.classList.remove('at-footer');
      return;
    }

    const footerTop = footer.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    // When footer is visible in the viewport (its top edge scrolls into view)
    // the button should stop being fixed and sit naturally above the footer
    if (footerTop <= windowHeight) {
      mobileOrder.classList.add('at-footer');
    } else {
      mobileOrder.classList.remove('at-footer');
    }
  }

  window.addEventListener('scroll', updateStickyOrder, { passive: true });
  window.addEventListener('resize', updateStickyOrder, { passive: true });
  updateStickyOrder(); // run on load
})();