/**
* Template Name: College
* Template URL: https://bootstrapmade.com/college-bootstrap-education-template/
* Updated: Jun 19 2025 with Bootstrap v5.3.6
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
      initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
      filters.addEventListener('click', function() {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        initIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

})();

/**
 * UYD Language Switching Function
 */
function switchLanguage(lang) {
  // Store the selected language in localStorage
  localStorage.setItem('selectedLanguage', lang);
  
  // You can implement actual language switching logic here
  // For now, we'll show an alert
  if (lang === 'sw') {
    alert('Kiswahili support coming soon! | Msaada wa Kiswahili unakuja hivi karibuni!');
  } else {
    alert('Language switched to English');
  }
  
  // In a full implementation, you would:
  // 1. Load appropriate language file
  // 2. Update all text content
  // 3. Potentially reload the page with language parameter
}

/**
 * UYD Impact Counter Animation
 */
document.addEventListener('DOMContentLoaded', function() {
  const counters = document.querySelectorAll('.impact-stat .number');
  
  const animateCounter = (counter) => {
    const target = parseInt(counter.textContent.replace(/[^0-9]/g, ''));
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60 FPS
    let current = 0;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        counter.textContent = counter.textContent.replace(/[0-9,]+/, target.toLocaleString());
        clearInterval(timer);
      } else {
        counter.textContent = counter.textContent.replace(/[0-9,]+/, Math.floor(current).toLocaleString());
      }
    }, 16);
  };
  
  // Use Intersection Observer to trigger animation when visible
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counter = entry.target.querySelector('.number');
        if (counter) {
          animateCounter(counter);
          observer.unobserve(entry.target);
        }
      }
    });
  });
  
  document.querySelectorAll('.impact-stat').forEach(stat => {
    observer.observe(stat);
  });

  /**
   * Initialize UYD data loading
   */
  window.addEventListener('load', function() {
    // Initialize data manager
    if (window.uydData) {
      window.uydData.init();
    }

    // Load events on events page
    if (document.body.classList.contains('events-page')) {
      if (window.uydData) {
        window.uydData.loadAllEvents();
      }
    }
  });

  /**
   * Handle form submissions for get-involved page
   */
  if (document.body.classList.contains('about-page') && window.location.pathname.includes('get-involved')) {
    // Newsletter form
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
      newsletterForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = {
          firstName: document.getElementById('newsletterFirstName').value,
          lastName: document.getElementById('newsletterLastName').value,
          email: document.getElementById('newsletterEmail').value,
          interests: Array.from(document.getElementById('newsletterInterests').selectedOptions).map(option => option.value)
        };

        try {
          await window.uydData.subscribeNewsletter(formData.email);
          alert('Thank you for subscribing to our newsletter!');
          newsletterForm.reset();
        } catch (error) {
          alert('There was an error subscribing. Please try again.');
        }
      });
    }

    // Volunteer form
    const volunteerForm = document.getElementById('volunteerForm');
    if (volunteerForm) {
      volunteerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your interest in volunteering! We will contact you soon.');
        volunteerForm.reset();
      });
    }

    // Partner form
    const partnerForm = document.getElementById('partnerForm');
    if (partnerForm) {
      partnerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your partnership interest! We will contact you soon.');
        partnerForm.reset();
      });
    }
  }

});